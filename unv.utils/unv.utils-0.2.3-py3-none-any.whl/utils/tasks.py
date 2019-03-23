import asyncio


def register(method):
    method.__task__ = True
    return method


class TaskSubprocessError(Exception):
    pass


class TasksBase:
    async def subprocess(self, command):
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if stderr:
            raise TaskSubprocessError(
                f'Command finished with error:\n{stderr.decode()}')
        if stdout:
            return stdout.decode()


class TasksManager:
    def __init__(self):
        self.tasks = {}

    def register(self, task_class, namespace: str = ''):
        namespace = namespace or task_class.__name__.lower() \
            .replace('tasks', '')
        self.tasks[namespace] = task_class

    def run_task(self, task_class, command, args):
        task = getattr(task_class(), command)
        return asyncio.run(task(*args))

    def run(self, command):
        args = command.split()
        namespace, command = args[0].split('.')

        task_class = self.tasks[namespace]
        task_args = []
        if len(args) > 1:
            task_args = args[1:]

        for method in dir(task_class):
            method = getattr(task_class, method)
            if getattr(method, '__task__', None) and \
                    method.__name__ == command:
                return self.run_task(task_class, command, task_args)
