import pika
from django.conf import settings

__all__ = (
    'get_broker_connection',
    'get_func_full_path',
)


def get_broker_connection():
    conn_params = pika.URLParameters(settings.BROKER_URL)
    return pika.BlockingConnection(conn_params)


def get_func_full_path(func):
    return f'{func.__module__}.{func.__name__}'
