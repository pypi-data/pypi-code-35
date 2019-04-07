import functools
from typing import Callable


def check_auth(func: Callable) -> Callable:
    """
    Decorator that ensures auth has been run before calling func
    Args:
        func: The decorated function
    """
    @functools.wraps(func)
    def wrapper_check_auth(*args, **kwargs):
        if args[0].token is None:
            raise AssertionError('Cannot run {} before performing auth flow'.format(func.__name__))
        value = func(*args, **kwargs)
        return value
    return wrapper_check_auth
