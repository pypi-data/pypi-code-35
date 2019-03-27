import asyncio


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

    def run_task(self, task_class, command, args):
        task = getattr(task_class(self.storage), command)
        return asyncio.run(task(*args))

    def run(self, commands):
        commands = commands.split()
        for index, command in enumerate(commands, start=1):
            namespace, task = command.split('.')
            task_class = self.tasks[namespace]

            task_args = []
            if ':' in task:
                task, task_args = task.split(':')
                task_args = task_args.split(',')

            for method in dir(task_class):
                method = getattr(task_class, method)
                if getattr(method, '__task__', None) and \
                        method.__name__ == task:
                    result = self.run_task(task_class, task, task_args)
                    if index == len(commands):
                        self.storage.clear()
                        return result
