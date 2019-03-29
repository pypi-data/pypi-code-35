import functools
from typing import Callable


__enveloop_number_of_loops__ = {}


def limit_recursion_to(number_of_loops: int = 100,
                       callback: Callable = None) -> Callable:
    """Decorator for any function or method that prevents infinite recursions.
    :param number_of_loops: number of loops after execution terminates
    :param callback: run in case of infinite recursion
    :return: function
    """

    def receive_fn(fn: Callable):
        """Function that receives main recursive function.
        :param fn: a recursive function
        :return: function
        """

        global __enveloop_number_of_loops__

        __enveloop_number_of_loops__[fn.__name__] = number_of_loops

        @functools.wraps(fn)
        def wrapper_fn(*args, **kwargs):
            """Function that does the actual wrapping.
            :param args:
            :param kwargs:
            :return: function response
            """

            if __enveloop_number_of_loops__[fn.__name__] > 0:
                __enveloop_number_of_loops__[fn.__name__] -= 1
                return fn(*args, **kwargs)
            else:
                del __enveloop_number_of_loops__[fn.__name__]
                if callback:
                    return callback(*args, **kwargs)

        return wrapper_fn

    return receive_fn
