import pytest
import os

from skidward.web import app, security_login_processor, user_data_store
from skidward.models import db, Role, Task, User, Worker


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


@pytest.fixture()
def test_admin_client(test_client, init_database):
    admin_user = User(email="admin@admin.com", username="admin", password="admin")
    db.session.add(admin_user)
    admin_role = Role(name="admin")
    db.session.add(admin_role)
    user_data_store.add_role_to_user("admin@admin.com", "admin")
    db.session.commit()

    test_client.post(
        "/login",
        data=dict(email="admin@admin.com", password="admin"),
        follow_redirects=True,
    )

    yield test_client


@pytest.fixture()
def pass_security_context_processor():
    with app.app_context():
        yield security_login_processor
