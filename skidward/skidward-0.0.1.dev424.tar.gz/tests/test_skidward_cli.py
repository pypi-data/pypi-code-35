import os
from signal import SIGTERM
from datetime import datetime, timedelta

import pytest

from .mock_objects import mock_get_all_workers_on_namespace
from skidward.__main__ import CLICommands, _detect_new_workers
from skidward.models import db, Worker, User, Task, Role, Job, Message
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

        db.session.add_all((worker, task_one, task_two))
        db.session.commit()

    pid_one = CLICommands.start_scheduler(True)
    pid_two = CLICommands.start_scheduler(True)

    assert pid_one is not pid_two

    # Cleanup running processes
    os.kill(pid_one, SIGTERM)
    os.kill(pid_two, SIGTERM)


@pytest.mark.parametrize(
    ("email"), ("dink@dink.com", "admin@skidward.com", "@testerthingy", "blabla@")
)
def test_admin_can_be_created(monkeypatch, app, email):
    monkeypatch.setattr("getpass.getpass", lambda x: "password")
    with app.app_context():
        test_ensure_test_database(app)

        assert len(db.session.query(User).all()) == 0
        CLICommands.create_admin(email)
        assert db.session.query(User).all()


@pytest.mark.parametrize(
    ("email"), ("", None, 123, "@", [], {}, ("valid@email.com", "but@itsatuple.com"))
)
def test_admin_can_not_be_created_with_invalid_email(monkeypatch, app, email):
    monkeypatch.setattr("getpass.getpass", lambda x: "password")
    with app.app_context():
        test_ensure_test_database(app)

        assert len(db.session.query(User).all()) == 0
        CLICommands.create_admin(email)
        assert len(db.session.query(User).all()) == 0


def test_existing_user_can_be_upgraded_to_admin(monkeypatch, app):
    monkeypatch.setattr("getpass.getpass", lambda x: "password")
    monkeypatch.setattr("click.confirm", lambda x: True)
    with app.app_context():
        test_ensure_test_database(app)

        email = "user@mail.com"
        role_end_user = Role(name="end_user")
        role_admin = Role(name="admin")
        user = User(
            email=email, username=email, password="password", roles=[role_end_user]
        )

        db.session.add_all((role_end_user, role_admin, user))

        assert "end_user" in user.roles
        assert "admin" not in user.roles

        CLICommands.create_admin(email)
        assert "admin" in user.roles


def test_database_can_be_migrated(app):
    with app.app_context():
        test_ensure_test_database(app)

        try:
            CLICommands.migrate()
        except Exception as e:
            pytest.fail("Migrations could not be applied.\n{}".format(e))


def test_making_migrations_works(app):
    with app.app_context():
        test_ensure_test_database(app)

        try:
            CLICommands.make_migrate()
        except Exception as e:
            pytest.fail("Migrations could not be created.\n{}".format(e))


def test_flush_tables(app):
    with app.app_context():
        worker = Worker(name="Test_worker", description="Some test worker.")
        task = Task(name="Test task", worker_id=worker.id, worker=worker)

        eight_days_ago = datetime.now() - timedelta(days=7)
        seven_days_ago = datetime.now() - timedelta(days=6)
        three_days_ago = datetime.now() - timedelta(days=3)

        job_one = Job(task_id=task.id, ran_at=eight_days_ago, task=task)
        job_two = Job(task_id=task.id, ran_at=seven_days_ago, task=task)
        job_three = Job(task_id=task.id, ran_at=three_days_ago, task=task)

        message_one = Message(job_id=job_one.id, job=job_one)
        message_two = Message(job_id=job_one.id, job=job_one)
        message_three = Message(job_id=job_three.id, job=job_three)

        db.session.add_all(
            (
                worker,
                task,
                job_one,
                job_two,
                job_three,
                message_one,
                message_two,
                message_three,
            )
        )

        # Make sure all jobs and messages exist
        original_jobs = Job.query.all()
        original_messages = Message.query.all()

        assert len(original_jobs) == 3
        assert len(original_messages) == 3

        # Delete messages older than 7 days from now
        CLICommands.flush_tables(7)
        assert len(Job.query.all()) == 2
        assert len(Message.query.all()) == 1

        assert not Job.query.get(job_one.id)
        assert not Message.query.filter(Message.job_id == job_one.id).all()

        assert Job.query.get(job_two.id)
        assert Job.query.get(job_three.id)

        # Delete messages older than 4 days from now
        CLICommands.flush_tables(4)
        assert len(Job.query.all()) == 1
        assert len(Message.query.all()) == 1

        assert not Job.query.get(job_two.id)
        assert not Message.query.filter(Message.job_id == job_two.id).all()

        assert not Job.query.get(job_two.id)
        assert Job.query.get(job_three.id)
        assert Message.query.all()
