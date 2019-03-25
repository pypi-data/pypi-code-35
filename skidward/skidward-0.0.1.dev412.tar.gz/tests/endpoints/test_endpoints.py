from unittest import mock

from flask_login import current_user

from skidward.models import Job, Message, Task, User, Worker


def test_it_loads_the_app(test_client, pass_security_context_processor):
    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_it_requires_login_to_access_home_page(
    test_client, pass_security_context_processor
):
    with test_client:
        response = test_client.get("/", follow_redirects=True)
        assert b"Login" in response.data


def test_it_logs_in_correct_user(test_client, init_database):
    with test_client:
        response = test_client.post(
            "/login",
            data=dict(email="test@test.com", password="123"),
            follow_redirects=True,
        )
        assert current_user.email == "test@test.com"


def test_it_creates_new_user_in_the_database(test_client, init_database):
    user = User.query.filter_by(email="test@test.com").first()
    assert user is not None
    assert user.email == "test@test.com"
    assert user.username == "testuser"


def test_it_redirects_to_admin_interface_on_login(test_client, init_database):
    response = test_client.post(
        "/login",
        data=dict(email="test@test.com", password="123"),
        follow_redirects=True,
    )
    assert b"Logged in as" in response.data


def test_it_logs_out_correctly_and_redirects_to_login(
    test_client, pass_security_context_processor
):
    with test_client:
        response = test_client.get("/logout", follow_redirects=True)
        assert response.status_code == 200
        assert b"Login" in response.data


def test_configure_asks_for_context_and_save_in_db_correctly(
    test_client, init_database
):
    test_client.post(
        "/login",
        data=dict(email="test@test.com", password="123"),
        follow_redirects=True,
    )
    response = test_client.get("/admin/task/configure/1", follow_redirects=True)
    assert b"Add Configuration" in response.data
    test_client.post(
        "/admin/task/configure/1",
        data=dict(key="new_key", value="new_value"),
        follow_redirects=True,
    )
    task = Task.query.get(1)
    assert task.context == {"new_key": "new_value"}
    assert type(task.context) == dict


@mock.patch("skidward.backend.RedisDummyBackend")
def test_configured_run_takes_new_context_but_does_not_save_in_db(
    mock_redis, backend, test_client, init_database
):
    test_client.post(
        "/login",
        data=dict(email="test@test.com", password="123"),
        follow_redirects=True,
    )
    mock_redis.return_value = backend
    response = test_client.post(
        "/admin/task/configure/1?temp_run=True",
        data=dict(key="tmp_key", value="tmp_value"),
        follow_redirects=True,
    )
    task_id, context = backend.hmget(
        "CONFIGURED_RUN", keys=["task_id", "overwrite_context"]
    )
    assert context == "{'tmp_key': 'tmp_value'}"
    task = Task.query.get(1)
    assert task.context == {"test_key": "test_value"}


@mock.patch("skidward.backend.RedisDummyBackend")
def test_quick_run_pushes_task_id_to_redis(
    mock_redis, test_client, backend, init_database
):
    test_client.post(
        "/login",
        data=dict(email="test@test.com", password="123"),
        follow_redirects=True,
    )
    mock_redis.return_value = backend
    response = test_client.get("/admin/task/run/1", follow_redirects=True)
    redis_tasks = backend.lrange("MANUAL_RUN", 0, -1)
    assert response.status_code == 200
    assert "1" in redis_tasks


@mock.patch("skidward.backend.RedisDummyBackend")
def test_configured_run_pushes_dict_of_task_with_context_to_redis(
    mock_redis, test_client, backend, init_database
):
    test_client.post(
        "/login",
        data=dict(email="test@test.com", password="123"),
        follow_redirects=True,
    )
    mock_redis.return_value = backend
    test_client.post(
        "admin/task/configure/1?temp_run=True",
        data=dict(key="tmp_key", value="tmp_value"),
        follow_redirects=True,
    )
    task_id, context = backend.hmget(
        "CONFIGURED_RUN", keys=["task_id", "overwrite_context"]
    )
    assert context == "{'tmp_key': 'tmp_value'}"


def test_manual_run_redirects_to_configure_if_no_context_is_present(
    test_client, init_database
):
    test_client.post(
        "/login",
        data=dict(email="test@test.com", password="123"),
        follow_redirects=True,
    )
    worker = Worker.query.first()
    new_task = Task(name="New_Task", worker=worker)
    init_database.session.add(new_task)
    init_database.session.commit()
    task = Task.query.filter_by(name="New_Task").first()
    assert task is not None
    assert task.id == 2
    assert not task.context
    response = test_client.get("/admin/task/run/2", follow_redirects=True)
    assert b"Add Configuration" in response.data


def test_end_user_has_no_access_to_user_view_and_get_redirected(
    test_client, init_database
):
    response = test_client.get("admin/user/")

    assert response.status_code == 302
    assert response.location == "http://localhost/login"


def test_admin_has_access_to_user_view(test_admin_client, init_database):
    response = test_admin_client.get("admin/user/")

    assert response.status_code == 200


def test_to_get_logs_from_db_when_no_longer_in_redis(
    test_admin_client, init_database, backend
):
    logged_message = "Logging job test"
    task = Task.query.one()
    job = Job(task_id=task.id)
    init_database.session.add(job)
    init_database.session.commit()

    message = Message(job_id=job.id, content=logged_message)
    init_database.session.add(message)
    init_database.session.commit()

    response = test_admin_client.get("admin/logs/get_logs/{}".format(job.id))

    assert response.status_code == 200
    assert response.json == [logged_message]


@mock.patch("skidward.web.views.get_redis_backend")
def test_to_get_logs_from_redis(mock_redis, test_admin_client, init_database, backend):
    mock_redis.return_value = backend

    logged_message = "Logging job test"
    task = Task.query.one()
    task.context = {"LOGGING_KEY": "TEST"}
    job = Job(task_id=task.id)
    init_database.session.add(job)
    init_database.session.commit()

    backend.lpush("TEST", logged_message)

    response = test_admin_client.get("admin/logs/get_logs/{}".format(job.id))

    assert response.status_code == 200
    assert response.json == [logged_message]


def test_calling_logs_endpoint(test_admin_client, init_database):
    task = Task.query.one()
    job = Job(task_id=task.id)
    init_database.session.add(job)
    init_database.session.commit()

    response = test_admin_client.get("admin/logs/logs/{}".format(job.id))

    assert response.status_code == 200
    assert response.content_type == "text/html; charset=utf-8"
