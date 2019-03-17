from datetime import datetime as dt
from unittest import mock

import pytest

from skidward.models import Task, Worker
from skidward.scheduler import scheduler


class TestElector:
    @mock.patch("skidward.scheduler.scheduler.CronExpression.check_trigger")
    def test_when_a_task_is_runner_elected_for_task(
        self, mock_cron, init_database, backend
    ):
        mock_cron.return_value = True

        elector = scheduler.Elector(backend)
        assert elector.is_runner_elected_for_task(Task.query.one())

    @mock.patch("skidward.scheduler.scheduler.CronExpression.check_trigger")
    def test_when_a_task_is_not_ready_to_run(self, mock_cron, init_database, backend):
        mock_cron.return_value = False

        elector = scheduler.Elector(backend)
        assert not elector.is_runner_elected_for_task(Task.query.one())

    @mock.patch("skidward.scheduler.scheduler.CronExpression.check_trigger")
    def test_task_is_not_ready_when_already_exists_in_redis(
        self, mock_cron, init_database, backend
    ):
        mock_cron.return_value = True

        date_mask = "-".join(map(str, dt.utcnow().timetuple()[:5]))
        task = Task.query.one()
        unique_key = f"{task.id}-{date_mask}"
        backend.set(unique_key, "host_1", ex=5, nx=True)

        elector = scheduler.Elector(backend)
        assert not elector.is_runner_elected_for_task(task)

    @mock.patch("skidward.backend.RedisDummyBackend.exists")
    @mock.patch("skidward.scheduler.scheduler.CronExpression.check_trigger")
    def test_task_is_not_ready_if_another_scheduler_holds_it(
        self, mock_cron, mock_redis_exists, init_database, backend
    ):
        mock_cron.return_value = True
        mock_redis_exists.return_value = False

        date_mask = "-".join(map(str, dt.utcnow().timetuple()[:5]))
        task = Task.query.one()
        unique_key = f"{task.id}-{date_mask}"
        backend.set(unique_key, "host_1", ex=5, nx=True)

        elector = scheduler.Elector(backend)
        assert not elector.is_runner_elected_for_task(Task.query.one())

    @pytest.mark.parametrize("length, ready", [(1, True), (0, False)])
    @mock.patch("skidward.scheduler.scheduler.Elector.is_runner_elected_for_task")
    def test_get_list_of_eligible_tasks(
        self, mock_ready, length, ready, init_database, backend
    ):
        mock_ready.return_value = ready

        elector = scheduler.Elector(backend)
        eligible_tasks = elector.get_elected_tasks(Task.query.all())
        assert len(eligible_tasks) == length

    def test_get_manual_task_if_available_in_redis_channel(
        self, backend, init_database
    ):
        task_id = Task.query.one().id
        backend.lpush("MANUAL_RUN", task_id)

        elector = scheduler.Elector(backend)
        yield_task = next(elector.get_manual_tasks())
        assert isinstance(yield_task, Task)
        assert yield_task.id == task_id

    def test_do_not_get_manual_task_if_not_available_in_redis_channel(
        self, backend, init_database
    ):
        task = Task.query.one()

        elector = scheduler.Elector(backend)
        with pytest.raises(StopIteration):
            next(elector.get_manual_tasks())

    @mock.patch("skidward.scheduler.scheduler.Elector.get_elected_tasks")
    def test_get_scheduled_task_if_eligible(self, mock_elected, init_database, backend):
        task = Task.query.one()
        mock_elected.return_value = [task]

        elector = scheduler.Elector(backend)
        yield_task = next(elector.get_scheduled_tasks())
        assert isinstance(yield_task, Task)
        assert yield_task.id == task.id

    @mock.patch("skidward.scheduler.scheduler.Elector.get_elected_tasks")
    def test_do_not_get_scheduled_task_if_not_eligible(
        self, mock_elected, backend, init_database
    ):
        mock_elected.return_value = []

        elector = scheduler.Elector(backend)
        with pytest.raises(StopIteration):
            next(elector.get_scheduled_tasks())

    @mock.patch("skidward.scheduler.scheduler.Elector.get_scheduled_tasks")
    @mock.patch("skidward.scheduler.scheduler.Elector.get_manual_tasks")
    def test_get_manual_and_schedule_tasks(
        self, mock_schedule, mock_manual, backend, init_database
    ):
        task = Task.query.one()
        worker = Worker.query.one()

        task_two = Task(
            name="task_2",
            worker_id=worker.id,
            context={"setting_1": "value_1"},
            cron_string="*/2 * * * *",
        )
        init_database.session.add(task_two)
        init_database.session.commit()

        mock_schedule.return_value = iter([task])
        mock_manual.return_value = iter([task_two])

        elector = scheduler.Elector(backend)
        tasks = elector.get_tasks()
        yield_task = next(tasks)
        assert isinstance(yield_task, Task)
        assert yield_task.id == task_two.id

        yield_task = next(tasks)
        assert isinstance(yield_task, Task)
        assert yield_task.id == task.id

    @mock.patch("skidward.scheduler.scheduler.Elector.get_scheduled_tasks")
    @mock.patch("skidward.scheduler.scheduler.Elector.get_manual_tasks")
    def test_get_manual_task_but_not_scheduled_as_not_available(
        self, mock_schedule, mock_manual, backend, init_database
    ):
        worker = Worker.query.one()
        task_two = Task(
            name="task_2",
            worker_id=worker.id,
            context={"setting_1": "value_1"},
            cron_string="*/2 * * * *",
        )
        init_database.session.add(task_two)
        init_database.session.commit()

        mock_schedule.return_value = None
        mock_manual.return_value = iter([task_two])

        elector = scheduler.Elector(backend)
        tasks = elector.get_tasks()
        yield_task = next(tasks)
        assert isinstance(yield_task, Task)
        assert yield_task.id == task_two.id

        with pytest.raises(TypeError):
            next(tasks)
