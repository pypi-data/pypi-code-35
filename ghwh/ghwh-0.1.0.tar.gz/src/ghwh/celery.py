from celery import Celery
from flask import Flask

from . import config


def init_celery(app: Flask) -> Celery:
    """Initialize Celery application.

    Args:
        app: Flask app.

    Returns:
        Celery app.
    """
    app.config.update(
        CELERY_BROKER_URL=config.celery_broker,
        CELERY_RESULT_BACKEND=config.celery_backend,
    )
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
