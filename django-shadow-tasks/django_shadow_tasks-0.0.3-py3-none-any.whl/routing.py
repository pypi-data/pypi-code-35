
__all__ = ('TasksRouter',)


class TasksRouter:
    """
    Кастомный роутер для отложенных задач, который раскидывает
    задачи по разным очередям.
    """

    @classmethod
    def get_routing_key_for_task(cls, task_name):
        """Маршрутизирует задачи по очередям.

        Примечание: с аргументами в исходниках и документации все напутано,
            поэтому пришлось подстроиться.

        Args:
            task_name(str): path to task
        """
        from shadow_tasks.settings import shadow_settings

        for routing_key, tasks in shadow_settings.QUEUE_TASKS_MAP.items():
            # TODO: add checking by wildcard
            if task_name in tasks:
                return routing_key

        return shadow_settings.DEFAULT_QUEUE
