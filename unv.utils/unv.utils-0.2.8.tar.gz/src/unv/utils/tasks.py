import asyncio
import functools


def register(method):
    method.__task__ = True
    return method


class TaskRunError(Exception):
    pass


class TasksBase:
    def __init__(self, storage):
        self._storage = storage

    async def _local(self, command):
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if stderr and proc.returncode != 0:
            raise TaskRunError(
                f'Command "{command}" finished with '
                f'error code [{proc.returncode}]:\n'
                f'{stderr.decode()} '
            )
        if stdout:
            return stdout.decode()


class TasksManager:
    def __init__(self):
        self.tasks = {}
        self.storage = {}

    def register(self, task_class, namespace: str = ''):
        namespace = namespace or task_class.__name__.lower() \
            .replace('tasks', '')
        self.tasks[namespace] = task_class

    def run_task(self, task_class, name, args):
        task = getattr(task_class(self.storage), name)
        return asyncio.run(task(*args))

    def run(self, commands):
        commands = commands.split()
        for index, command in enumerate(commands, start=1):
            namespace, name = command.split('.')

            task_class = self.tasks[namespace]
            args = []
            if ':' in name:
                name, task_args = name.split(':')
                args = task_args.split(',')

            method = getattr(task_class, name)
            if getattr(method, '__task__', None) and name == method.__name__:
                result = self.run_task(task_class, name, args)
                if index == len(commands):
                    self.storage.clear()
                    return result
