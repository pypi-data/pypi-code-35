from typing import Callable, Optional


def curry(func: Callable, arg_count: Optional[int] = None) -> Callable:
    """
    Curry Decorator
    """
    if arg_count is None:
        arg_count = func.__code__.co_argcount

    def p(*args):
        if len(args) == arg_count:
            return func(*args)

        def q(*b):
            return func(*(args + b))

        return curry(q, arg_count - len(args))

    return p
