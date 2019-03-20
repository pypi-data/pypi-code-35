import importlib
from django.conf import settings

__all__ = ('TaskRegistry',)


class TaskRegistryError(Exception):
    pass


class TaskRegistry:
    registry = set()

    @classmethod
    def add_task(cls, f_path):
        cls.registry.add(f_path)

    @classmethod
    def discover_tasks(cls):
        """Load tasks from apps.<>.tasks to register them in `cls.registry`."""
        local_apps = settings.LOCAL_APPS

        for app in local_apps:
            try:
                importlib.import_module(f'{app}.tasks')
            except ImportError:
                continue
