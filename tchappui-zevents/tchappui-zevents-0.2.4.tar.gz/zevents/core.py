# -*- coding: utf-8 -*-

"""Implements the ZEvents core system.
"""

from collections import defaultdict, OrderedDict
import queue
import weakref
import inspect
import threading
from contextlib import contextmanager


class EventManager:
    """Class responsible for the mechanics of event management.

    EventManager provides the interface to subscribe or unsubscribe a
    handler to or from the notification feed of events of different types. This
    class also provides the method to fire an event object.
    """

    def __init__(self):
        self._lock = threading.Lock()
        # Subscribers dictionnary. Keys are event types. Values are Orderdicts
        # of weakly-referenced functions or methods
        self._subscribers = defaultdict(OrderedDict)

        # Queues for pending subscriptions, unsubscription and notifications
        self._subscriptions = queue.Queue()
        self._unsubscriptions = queue.Queue()
        self._notifications = queue.Queue()

    def send(self, event):
        """Sends an event notification to all the subscribers."""
        self._notifications.put([type(event), event])
        # Process the queued subscription, unsubscription and notification
        # requests
        with self._non_blocking_lock() as locked:
            if locked:
                self._process_requests('subscriptions')
                self._process_requests('unsubscriptions')
                self._notify()

    def subscribe(self, event_type, handler):
        """Subscribes a handler function to the notification feed of a given
        event.
        """
        self._subscriptions.put([event_type, handler])

    def unsubscribe(self, event_type, handler):
        """Unsubscribes a handler function from the notification feed of a
        given event.
        """
        self._unsubscriptions.put([event_type, handler])

    def _process_requests(self, action):
        """Processes pending subscriptions."""
        # We empty the subscription queue
        queue = getattr(self, f'_{action}')
        while not queue.empty():
            event_type, handler = queue.get()
            ref = weakref.ref
            if inspect.ismethod(handler) and hasattr(handler, '__self__'):
                ref = weakref.WeakMethod
            weak_handler = ref(handler)
            # We subscribe the handler to all superclass events
            for klass in event_type.__mro__:
                if action == 'subscriptions' and issubclass(klass, Event):
                    self._subscribers[klass][weak_handler] = True
                elif (
                    action == 'unsubscriptions' and
                    weak_handler in self._subscribers[klass]
                ):
                    del self._subscribers[klass][weak_handler]


    def _notify(self):
        """Processes pending notifications."""
        # We Empty the notification queue
        while not self._notifications.empty():
            event_type, event = self._notifications.get()
            for weak_handler in self._subscribers[event_type]:
                handler = weak_handler()
                handler(event)

    @contextmanager
    def _non_blocking_lock(self):
        """Context manager for non-blocking acquisition of self._lock."""
        locked = self._lock.acquire(blocking=False)
        try:
            yield locked
        finally:
            if locked:
                self._lock.release()


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
