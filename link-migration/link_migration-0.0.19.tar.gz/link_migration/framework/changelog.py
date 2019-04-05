
import os

from functools import wraps
from pathlib import Path

__all__ = [
    'changelog'
]


class ChangeLog:
    def __init__(self, output):
        self.output = output

    def record(self, *args):
        with open(self.output, "a") as write:
            write.write(','.join([f'"{str(arg)}"' for arg in args]) + '\n')

    def cleanup(self):
        print('do something')


def changelog(output):
    def decorator(func):
        @wraps(func)
        def wrapper(self):
            path = Path(str(self.config.MIGRATIONS_ABS_PATH) + output).resolve()
            try:
                os.makedirs(path.parent)
            except:
                pass
            path.touch()

            change = ChangeLog(path)
            func(self, output=change)
            change.cleanup()
        return wrapper
    return decorator
