from typing import Callable, Any
from functools import wraps


__all__ = [
    'state_modifier',
]

def state_modifier(result_factory:Callable, state_updater:Callable[[Any, Any], Any]):
    """

    :param result_factory:
    :param state_updater:
    :return:
    """
    def inner_decorator(f_to_wrap:Callable):
        @wraps(result_factory)
        def f_that_gets_called(*args, **kwargs):
            state_updater(args[0], result_factory(*args[1:], **kwargs))
            return f_to_wrap(args[0])
        return f_that_gets_called
    return inner_decorator
