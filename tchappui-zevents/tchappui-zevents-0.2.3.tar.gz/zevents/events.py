# -*- coding: utf-8 -*-

"""Module defining standard events for the ZEvents system."""

from .manager import EventManager

class Event:
    """Base class of all events in the notification system.

    Event is the base class used to create all the specialized events. It
    provides default implementations to send notification for the underlying
    event or to subscribe/unsubscribe to/from the notification feed of this
    particular event.
    """

    manager = EventManager()

    def __init__(self):
        """Default constructor."""
        self.name = 'Generic Event'

    @classmethod
    def send(cls, *args, **kargs):
        """Sends a notification to all the subscribers listening to this event.
        """
        event = cls(*args, **kargs)
        cls.manager.send(event)

    @classmethod
    def subscribe(cls, handler):
        """Subscribes a handler function to the notification feed of this event.
        """
        cls.manager.subscribe(cls, handler)

    @classmethod
    def unsubscribe(cls, handler):
        """Unsubscribes a handler function from the notification feed of this
        event.
        """
        cls.manager.unsubscribe(cls, handler)

    @classmethod
    def listen(cls, func):
        params = list(inspect.signature(func).parameters.keys())
        if len(params) == 1:
            # This is a normal function
            cls.subscribe(func)
        elif len(params) == 2 and params[0] == 'self':
            # This is an unbound instance function
            if not hasattr(func, "_zevents"):
                setattr(func, "_zevents", [])
            func._zevents.append(cls)
        else:
            raise TypeError(
                f"Cannot subscribe {func.__qualname__}. Incorrect signature."
            )

        return func

    def __str__(self):
        """Converts the current event to a string representation."""
        return f'<{type(self).__name__} at {id(self)}>'



class TickEvent(Event):
    """Event raised by an application-level event loop."""

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.name = "Tick Event"


class QuitEvent(Event):
    """Event raised to quit an application-level event loop."""

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.name = "Quit Event"
