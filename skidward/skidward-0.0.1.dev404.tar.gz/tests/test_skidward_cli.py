import os
from signal import SIGTERM

import pytest

from .mock_objects import mock_get_all_workers_on_namespace
from skidward.__main__ import CLICommands, _detect_new_workers
from skidward.models import db, Worker, User, Task
import skidward.worker_detector as wd


def test_ensure_test_database(app):
    assert "skidwardDB_TEST" in app.config["SQLALCHEMY_DATABASE_URI"]


def test_detect_new_workers(monkeypatch, app):
    monkeypatch.setattr(
        wd, "get_all_workers_on_namespace", mock_get_all_workers_on_namespace
    )
    with app.app_context():
        test_ensure_test_database(app)

        expected_result = ["real_name", "other_name"]
        actual_result = _detect_new_workers()

        assert len(expected_result) == len(actual_result)
        assert expected_result.pop() in actual_result
        assert expected_result.pop() in actual_result


def test_workers_publishable_in_db(monkeypatch, real_namespace, app):
    monkeypatch.setattr(
        wd, "get_all_workers_on_namespace", mock_get_all_workers_on_namespace
    )
    with app.app_context():
        test_ensure_test_database(app)

        workers_on_namespace = wd.get_all_workers_on_namespace(real_namespace)
        registered_workers = [w.name for w in db.session.query(Worker).all()]
        unregistered_workers = list(set(workers_on_namespace) - set(registered_workers))

        # Verify workers found different than ones in DB
        assert registered_workers is not None
        assert len(workers_on_namespace) > 0
        assert len(unregistered_workers) > 0

        CLICommands.publish_workers()

        new_registered_workers = [w.name for w in db.session.query(Worker).all()]
        new_unregistered_workers = list(
            set(workers_on_namespace) - set(new_registered_workers)
        )

        # Verify new workers registered in DB
        assert new_registered_workers is not None
        assert len(new_registered_workers) > 0
        assert len(new_unregistered_workers) == 0


def test_scheduler_spawns_new_processes(app):
    with app.app_context():
        worker = Worker(name="worker", description="A worker.")
        db.session.add(worker)
        db.session.commit()

        context = {"LOGGING_CHANNEL": "ch:channel"}
        task_one = Task(
            name="first_task",
            worker=worker,
            worker_id=worker.id,
            context=context,
            cron_string="",
        )
        task_two = Task(
            name="second_task",
            worker=worker,
            worker_id=worker.id,
            context=context,
            cron_string="",
        )

        db.session.add(task_one)
        db.session.add(task_two)
        db.session.commit()

    pid_one = CLICommands.start_scheduler(True)
    pid_two = CLICommands.start_scheduler(True)

    assert pid_one is not pid_two

    # Cleanup running processes
    os.kill(pid_one, SIGTERM)
    os.kill(pid_two, SIGTERM)


@pytest.mark.parametrize(
    ("email"), ("dink@dink.com", "admin@skidward.com", "admin", "", 123)
)
def test_create_admin(monkeypatch, app, email):
    monkeypatch.setattr("getpass.getpass", lambda x: "password")
    with app.app_context():
        test_ensure_test_database(app)

        try:
            assert len(db.session.query(User).all()) == 0
            CLICommands.create_admin(email)
            assert db.session.query(User).all() is not None
        except Exception:
            pytest.fail("Admin could not be created.")
