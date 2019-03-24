"""
Provides EventEmitter class.
"""

import asyncio
from functools import partial
from typing import (
    Callable,
    Dict,
    Type,
    Union,
    Coroutine,
    Set,
)

from .event import BaseEvent
from .subscription import Subscription


# pylint: disable=invalid-name
EventCallbackType = Callable[[BaseEvent], Union[None, Coroutine[None, None, None]]]


class EventEmitter:
    """
    ABC for a class whose instances emit events.

    :ivar _event_listeners: A dictionary whose keys are subclasses of BaseEvent
            and whose values are lists of event handlers. Event handlers should
            be callables that accept a single argument: the event being emitted.
    """

    _subscriptions: Dict[Type[BaseEvent], Set[Subscription]]

    def __init__(
            self,
            *args,
            loop: "asyncio.AbstractEventLoop" = None,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._loop = loop or asyncio.get_event_loop()
        self._subscriptions = {}

    def listen(self, event_type: Type[BaseEvent], callback: EventCallbackType) -> "Subscription":
        """
        Register a callback to be fired when an event is emitted.
        :param event_type: The type of event (subclass of :py:class:`BaseEvent`)
                to listen for.
        :param callback: The callback to trigger when the event is emitted;
                should accept a single parameter which is the instance of
                `event_type` that was emitted.
        :return:
        """
        if event_type not in self._subscriptions:
            self._subscriptions[event_type] = set()
        subscription = Subscription(
            callback,
            unsubscribe=partial(self._remove_subscription, event_type),
            loop=self._loop,
        )
        self._subscriptions[event_type].add(subscription)
        return subscription

    def emit(self, event: BaseEvent):
        """
        Emit an event.
        :param event: The event to be omitted.
        :return:
        """
        if not isinstance(event, BaseEvent):
            raise ValueError(f"Events must be subclasses of BaseEvent (got {repr(event)}).")
        if event.target is None:
            event.target = self
        subscriptions = self._get_subscriptions_for_event_type(type(event))
        for subscription in subscriptions:
            subscription.invoke(event)

    def proxy(self, emitter):
        """
        Proxy events from another emitter.

        Useful in a grandparent-parent-child type pattern where the grandparent
        cares about events emitted in the child.
        :param emitter:
        :return:
        """
        emitter.listen(BaseEvent, self._proxy_event)

    def _proxy_event(self, event):
        """
        Emit an event via proxy.
        :param event: The event to proxy.
        :return:
        """
        self.emit(event)

    def _get_subscriptions_for_event_type(
            self, event_type: Type,
    ) -> Set["Subscription"]:
        """
        Get all handlers for an event type.

        This method will walk up the subclass graph so that a handler
        for `SomeEventType` will also handle events of type
        `SubclassOfSomeEventType`.
        :param event_type: The event type to find handlers for.
        :return: A list of event handlers.
        """
        # Note: See `test_event_multiple_inheritance.py` for a description about
        #       why we need to use a set here (rather than a list).
        handlers = set()
        if not issubclass(event_type, BaseEvent):
            raise ValueError(f"Event classes must extend BaseEvent (got {repr(event_type)}).")
        if event_type in self._subscriptions:
            handlers.update(self._subscriptions[event_type])
        for event_supertype in event_type.__bases__:
            if not issubclass(event_supertype, BaseEvent):
                continue
            handlers.update(self._get_subscriptions_for_event_type(event_supertype))
        return handlers

    def _remove_subscription(self, event_type: Type["BaseEvent"], subscription: "Subscription"):
        if event_type in self._subscriptions:
            if subscription in self._subscriptions[event_type]:
                self._subscriptions[event_type].remove(subscription)
