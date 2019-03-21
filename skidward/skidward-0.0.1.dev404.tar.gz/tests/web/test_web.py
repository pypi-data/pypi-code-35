import pytest

from skidward.app import app
from skidward.models import db


def test_it_creates_app():
    assert app


def test_db_initialized_with_app():
    assert db
    with app.app_context():
        assert db.get_app() == app


@pytest.mark.parametrize(
    "config_key",
    (
        "DEBUG",
        "FLASK_ADMIN_SWATCH",
        "SQLALCHEMY_DATABASE_URI",
        "SECRET_KEY",
        "SECURITY_PASSWORD_SALT",
        "SECURITY_PASSWORD_HASH",
        "SQLALCHEMY_TRACK_MODIFICATIONS",
    ),
)
def test_app_is_configured(config_key):
    with app.app_context():
        try:
            assert app.config[config_key] is not None
        except KeyError:
            pytest.fail(f"Key {config_key} not found in the app config.")
