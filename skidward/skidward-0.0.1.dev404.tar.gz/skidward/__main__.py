import os
import getpass
import multiprocessing

import fire
import click
from flask_security import utils

from skidward import worker_detector
from skidward.app import app
from skidward.web import user_data_store
from skidward.scheduler import scheduler
from skidward.models import db, Worker, Job


def _initialize_database():
    db.init_app(app)
    db.create_all()
    print("Database initialized.")


def _migrate_db_if_needed():
    # We currently do not support migrations, not sure if we want/need this
    # If we use Flask-migrate:

    # from flask-migrate import Migrate, migrate
    # migrations = Migrate(app, db)
    # migrate()
    print("Migrations not yet implemented.")
    pass


def _detect_new_workers() -> list:
    def _get_registered_workers() -> list:
        return [w.name for w in Worker.query.all()]

    unregistered_workers = []
    registered_workers = _get_registered_workers()
    detected_workers = worker_detector.get_all_workers_on_namespace()

    for dw in detected_workers:
        if dw not in registered_workers:
            unregistered_workers.append(dw)

    return unregistered_workers


def _insert_new_workers_in_database():
    new_workers = [Worker(name=worker) for worker in _detect_new_workers()]
    db.session.bulk_save_objects(new_workers)
    db.session.commit()


def _start_new_scheduler(is_background_process):
    if is_background_process:
        process = multiprocessing.Process(target=scheduler.start)
        process.start()
        return process.pid

    print(os.getpid())
    return scheduler.start()


def _create_admin_user(email):
    email = str(email)

    def _get_user_by_email():
        return user_data_store.find_user(email=email)

    def _set_admin_role_for_user():
        user_data_store.add_role_to_user(email, "admin")

    def _prompt_for_password():
        return utils.hash_password(getpass.getpass("Please enter your password: "))

    def _create_user():
        hashed_password = _prompt_for_password()
        username = email.split("@")[0]

        new_user = user_data_store.create_user(
            email=email, username=username, password=hashed_password
        )
        user_data_store.add_role_to_user(email, "admin")

        return new_user

    user_data_store.find_or_create_role(name="admin", description="Administrator")
    user_data_store.find_or_create_role(name="end-user", description="End user")

    existing_user = _get_user_by_email()
    if existing_user:
        if click.confirm("User exists. Upgrade to admin?"):
            _set_admin_role_for_user()
            print("User upgraded to admin.")

        return existing_user

    new_user = _create_user()
    _set_admin_role_for_user()
    db.session.commit()

    print("User created and set to admin.")

    return new_user


def _flush_tables():
    Job.delete_expired_entries()
    print("Flushed Job and Message tables' older entries.")


class CLICommands(object):
    @staticmethod
    def initdb():
        _initialize_database()

    @staticmethod
    def migrate():
        _migrate_db_if_needed()

    @staticmethod
    def publish_workers():
        _insert_new_workers_in_database()

    @staticmethod
    def synchronize(migrate=None):
        if migrate:
            _migrate_db_if_needed()

        _insert_new_workers_in_database()

    @staticmethod
    def create_admin(email):
        _create_admin_user(email)

    @staticmethod
    def start_scheduler(is_background_process=False):
        pid = _start_new_scheduler(is_background_process)
        print(f"Created a new scheduler with PID {pid}.")
        return pid

    @staticmethod
    def flush_tables():
        return _flush_tables()


def main():
    fire.Fire(CLICommands)


if __name__ == "__main__":
    with app.app_context():
        main()
