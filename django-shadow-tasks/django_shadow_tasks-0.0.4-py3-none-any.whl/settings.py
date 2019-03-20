import random

from datetime import timedelta

from django.conf import settings
from shadow_tasks.routing import TasksRouter

__all__ = ('shadow_settings',)


DEFAULT_SETTINGS = {
    'CONSUMER_SLEEP_TIMEOUT': 0.2,
    'CONSUMER_MAX_SLEEPING_TIME': random.choice(range(60, 60 * 10, 15)),
    # Set '' if task could be executed immediately. While testing for example
    'BROKER_URL': None,
    'EXCHANGE': 'default',
    'DLX_EXCHANGE': 'default_dlx',
    'DLX_TIMEOUT': int(timedelta(minutes=5).total_seconds()),
    'DLX_PER_QUEUE': True,
    'DLX_DEFAULT_QUEUE_NAME': 'dlx',
    'QUEUE_TASKS_MAP': {
        'default': []
    },
    'DEFAULT_QUEUE': 'default',
    'TASKS_ROUTER': TasksRouter,
}


class ShadowSettings:
    def __init__(self):
        self.user_settings = getattr(settings, 'SHADOW_TASKS', {})

    def __getattr__(self, attr):
        if attr not in DEFAULT_SETTINGS:
            raise AttributeError(f'Invalid shadow tasks setting: {attr}')

        try:
            value = self.user_settings[attr]
        except KeyError:
            value = DEFAULT_SETTINGS[attr]

        if value is None:
            raise AttributeError(f'Set shadow tasks setting: {attr}')

        return value


shadow_settings = ShadowSettings()

