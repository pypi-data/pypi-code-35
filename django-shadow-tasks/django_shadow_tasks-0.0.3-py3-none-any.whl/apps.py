from django.apps import AppConfig


class Config(AppConfig):
    name = 'shadow_tasks'
    verbose_name = 'Shadow tasks'

    def ready(self):
        from shadow_tasks.registry import TaskRegistry
        TaskRegistry.discover_tasks()
