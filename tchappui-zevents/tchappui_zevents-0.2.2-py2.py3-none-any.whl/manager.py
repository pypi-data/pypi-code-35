# -*- coding: utf-8 -*-

"""Implements the ZEvents core system.
"""

from collections import defaultdict, OrderedDict
import queue
import weakref
import inspect
import threading


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
        # Process the queued subscriptions, unsubscriptions and requests
        with self._lock:
            self._process_requests('subscription')
            self._process_requests('unsubscription')
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
        try:
            while True:
                event_type, handler = self._subscriptions.get(block=False)
                ref = weakref.ref
                if inspect.ismethod(handler) and hasattr(handler, '__self__'):
                    ref = weakref.WeakMethod
                weak_handler = ref(handler)
                # We subscribe the handler to all superclass events
                for klass in event_type.__mro__:
                    if action == 'subscription' and issubclass(klass, Event):
                        self._subscribers[klass][weak_handler] = True
                    elif (
                        action == 'unsubscription' and
                        weak_handler in self._subscribers[klass]
                    ):
                    del self._subscribers[klass][weak_handler]
        except queue.Queue.Empty:
            pass

    def _notify(self):
        """Processes pending notifications."""
        # We Empty the notification queue
        try:
            while True:
                event_type, event = self._notifications.get(block=False)
                with self._lock:
                    for weak_handler in self._subscribers[event_type]:
                        handler = weak_handler()
                        handler(event)
        except queue.Queue.Empty:
            pass


