import logging
import datetime
from unittest import mock

from skidward.app import app
from skidward.models import Job, JobStatus, Task, Worker
from skidward.task_runner import TaskRunner


@mock.patch("skidward.task_runner.TaskRunner.start")
def test_new_job_is_created(mock_start, init_database, monkeypatch):
    monkeypatch.setattr(
        TaskRunner,
        "_set_logging_config",
        (lambda x: logging.basicConfig(handlers=logging.NullHandler())),
    )
    with app.app_context():
        task = Task.query.all()[0]
        task_runner = TaskRunner(task.id)
        task_runner._create_new_job()

        assert init_database.session.query(Job).one().task.id == task.id


def test_unique_message_key_creation(init_database):
    test_worker = Worker(name="real_name")
    test_task = Task(
        name="task_1",
        worker=test_worker,
        context={"setting_1": "value_1"},
        cron_string="*/2 * * * *",
    )
    test_job = Job(task=test_task)
    init_database.session.commit()

    assert TaskRunner.get_unique_message_key(
        test_job.id, test_task.id
    ) == "J{}-T{}".format(test_job.id, test_task.id)


@mock.patch("skidward.worker_detector.create_namespace_module_manager")
def test_full_process_calling_run(mock_create, init_database, monkeypatch):
    monkeypatch.setattr(
        TaskRunner,
        "_set_logging_config",
        (lambda x, y: logging.basicConfig(handlers=logging.NullHandler())),
    )
    monkeypatch.setattr(
        TaskRunner,
        "_persist_logs",
        (lambda x, y, z: print("Things got saved to the DB.")),
    )
    monkeypatch.setattr(
        TaskRunner, "_expire_logs", (lambda x, y: print("Original list got expired."))
    )
    with app.app_context():
        task = Task.query.all()[0]
        context = {"LOGGING_KEY": "ch:channel"}
        task.context = context
        init_database.session.commit()

        TaskRunner(task.id)
        job = init_database.session.query(Job).one()

        mock_create.return_value.load_module.assert_called_once_with("real_name")
        mock_create.return_value.load_module.return_value.start.assert_called_once_with(
            {"LOGGING_KEY": "ch:channel"}
        )
        assert job.id == 1
        assert job.task_id == 1
        assert job.state == JobStatus.SUCCESS
        assert isinstance(job.ran_at, datetime.datetime)
