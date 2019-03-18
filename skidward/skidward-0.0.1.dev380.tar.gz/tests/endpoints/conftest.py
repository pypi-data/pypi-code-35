import pytest
import os

from skidward.web import app, security, security_login_processor
from skidward.models import db, User, Worker, Task


def create_app():
    app.config["TESTING"] = os.getenv("WEB_TESTING")
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    return app


@pytest.fixture()
def test_client():
    flask_app = create_app()
    client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield client
    ctx.pop()


@pytest.fixture()
def pass_security_context_processor():
    with app.app_context():
        yield security_login_processor


@pytest.fixture()
def init_database():
    db.create_all()
    user1 = User(email="test@test.com", username="testuser", password="123")
    db.session.add(user1)
    worker1 = Worker(name="Test_Worker")
    db.session.add(worker1)
    task1 = Task(name="Test_Task", worker=worker1, context={"test_key": "test_value"})
    db.session.add(task1)
    db.session.commit()
    yield db
    db.drop_all()
