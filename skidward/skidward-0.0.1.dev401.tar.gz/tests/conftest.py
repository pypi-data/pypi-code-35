import os

import pytest
from flask_security import Security, SQLAlchemyUserDatastore

from skidward.app import app as application
from skidward.models import db, User, Role, Task, Worker
from skidward.backend import get_redis_backend
from tests.mock_objects import MockNamespaceModuleManager


@pytest.fixture(autouse=True, scope="session")
def set_testing_state():
    os.environ["WEB_TESTING"] = "True"
    yield
    os.environ["WEB_TESTING"] = "False"


@pytest.fixture(scope="function")
def app(request):
    def cleanup_db():
        with application.app_context():
            db.session.rollback()
            db.drop_all()

    def set_test_db_in_application():
        with application.app_context():
            db_uri = application.config["SQLALCHEMY_DATABASE_URI"].split("/")
            db_uri[-1] = "skidwardDB_TEST"
            application.config["SQLALCHEMY_DATABASE_URI"] = "/".join(db_uri)

    with application.app_context():
        set_test_db_in_application()
        db.init_app(application)
        db.create_all()
        request.addfinalizer(cleanup_db)

        return application


@pytest.fixture()
def init_database():
    with application.app_context():
        db.create_all()
        worker_one = Worker(name="real_name")
        db.session.add(worker_one)
        db.session.commit()

        task_one = Task(
            name="task_1",
            worker=worker_one,
            context={"setting_1": "value_1"},
            cron_string="*/2 * * * *",
        )
        db.session.add(task_one)
        db.session.commit()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture
def real_namespace() -> str:
    return "skidward.real.name.space"


@pytest.fixture
def mock_namespace_module_manager() -> MockNamespaceModuleManager:
    return MockNamespaceModuleManager("skidward.real.name.space")


@pytest.fixture()
def backend(monkeypatch):
    monkeypatch.setenv("WEB_TESTING", "True")
    dummy_backend = get_redis_backend()
    yield dummy_backend
    dummy_backend.erase()
