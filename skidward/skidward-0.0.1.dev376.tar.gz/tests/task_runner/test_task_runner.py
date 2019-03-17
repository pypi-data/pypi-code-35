import logging
import datetime
from unittest import mock

from skidward.app import app
from skidward.models import Job, JobStatus, Task
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


@mock.patch("skidward.worker_detector.create_namespace_module_manager")
def test_full_process_calling_run(mock_create, init_database, monkeypatch):
    monkeypatch.setattr(
        TaskRunner,
        "_set_logging_config",
        (lambda x: logging.basicConfig(handlers=logging.NullHandler())),
    )
    with app.app_context():
        task = Task.query.all()[0]
        context = {"LOGGING_CHANNEL": "ch:channel"}
        task.context = context
        init_database.session.commit()

        TaskRunner(task.id)
        job = init_database.session.query(Job).one()

        mock_create.return_value.load_module.assert_called_once_with("real_name")
        mock_create.return_value.load_module.return_value.start.assert_called_once_with(
            {"LOGGING_CHANNEL": "ch:channel"}
        )
        assert job.id == 1
        assert job.task_id == 1
        assert job.state == JobStatus.SUCCESS
        assert isinstance(job.ran_at, datetime.datetime)
