# -*- coding: utf-8 -*-

"""Implements the decorators for easy subscriptions of methods to ZEvents
"""

from functools import wraps


def listener(cls):
    """Class decorator to mark a class as a zevent listener."""
    func = cls.__init__

    # Wraps the class constructor to automate the subscription of methods to
    # event handlers
    @wraps(cls.__init__)
    def new_init(self, *args, **kwargs):
        func(self, *args, **kwargs)
        # Subscribe methods in __dict__ marked as handler for a given
        # event type
        for key, obj in cls.__dict__.items():
            if hasattr(obj, "_zevents"):
                zevents = obj._zevents
                for zevent in zevents:
                    zevent.subscribe(getattr(self, key))

    # Patching the constructor
    cls.__init__ = new_init
    return cls

