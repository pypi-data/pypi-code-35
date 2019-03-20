import asyncio


def register(method):
    method.__task__ = True
    return method


class TaskErrorException(Exception):
    pass


class TasksBase:
    def __init__(self):
        self.tasks = {}

        for method in dir(self):
            method = getattr(self, method)
            if getattr(method, '__task__', None):
                self.tasks[method.__name__] = method


class TasksManager:
    def __init__(self):
        self.tasks = {}

    def register(self, task_class, namespace: str = ''):
        namespace = namespace or task_class.__name__.lower() \
            .replace('tasks', '')
        self.tasks[namespace] = task_class()

    def run(self, command):
        args = command.split()
        namespace, command = args[0].split('.')
        task = self.tasks[namespace].tasks[command]

        task_args = []
        if len(args) > 1:
            task_args = args[1:]

        return asyncio.run(task(*task_args))
