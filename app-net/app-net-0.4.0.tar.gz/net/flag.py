# -*- coding: utf-8 -*-
"""
Flag Module
-----------

Contains the flag decorator and should have nothing else.
"""

__all__ = [
    'flag'
]

# std imports
from functools import wraps

# package imports
import net


def flag(name):
    """
    Register a function as a flag handler for the peer server.

    :param name: str
    """

    def registry(func):
        @wraps(func)
        def handler(*args, **kwargs):
            return func(*args, **kwargs)

        # register the function with the peer handler
        net.Peer().register_flag(name, handler)

        return handler
    return registry
