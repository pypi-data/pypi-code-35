"""
Ensure that multiple inheritance doesn't double-call event handlers.

We need to handle the case where we walk up subclass graphs that isn't a tree
(that is, subclass graphs where two unique parents share a common ancestor).

For a concrete example, suppose you have LowBatteryEvent;
LowBatteryEvent is a subclass of WarningEvent and SystemStatusEvent,
both of which are subclasses of LaptopEvent*.
Suppose we register a listener for LaptopEvent and then dispatch a
LowBatteryEvent; when we traverse the subclass graph, we first find
all handlers specifically for LowBatteryEvent (none); then we search
for handlers for WarningEvent and SystemStatusEvent; since each of
these extend LaptopEvent, they both return our registered handler.
So if we simply created a list of handlers (or just recursively called
handlers), we would call the listener twice for the same event;
whereas by forming a set, we guarantee that we don't ever call a
single handler twice for the same event.

*This example is actually broken because it forms a class hierarchy diamond
and created an ambiguous MRO.
https://en.wikipedia.org/wiki/Multiple_inheritance#The_diamond_problem
"""

import asyncio

import pytest

from aioevent import (
    BaseEvent,
    EventEmitter,
    event_listener,
)

pytestmark = pytest.mark.asyncio


class MyEvent(BaseEvent):
    pass


class MyMixin(MyEvent):
    @property
    def foo(self):
        return "foo"


class SubEvent(MyEvent):
    """
    Note: This class is required to prevent ambiguous MRO.

    If :class:`SubEventOne` and :class:`SubEventTwo` directly subclassed
    :class:`MyEvent` (as well as :class:`MyMixin`), Python would complain
    about not being able to create a consistent method resolution order (MRO)
    for those two bases.
    """
    pass


class SubEventOne(SubEvent, MyMixin):
    @property
    def spam(self):
        return "spam"


class SubEventTwo(SubEvent, MyMixin):
    @property
    def eggs(self):
        return "eggs"


async def test_event_multiple_inheritance(event_loop: "asyncio.loop.AbstractEventLoop"):
    e = EventEmitter(loop=event_loop)
    queue = asyncio.Queue(loop=event_loop)

    @event_listener(e, MyEvent)
    def on_event(event: "MyEvent"):
        queue.put_nowait(event)

    e.emit(SubEventOne())
    assert isinstance(await queue.get(), SubEventOne)

    # If multiple inheritance is broken, the queue will not be empty since the
    # handler will have been invoked twice (once from the path
    # SubEventOne -> SubEvent -> MyEvent, and once from the path
    # SubEventOne -> MyMixin -> MyEvent).
    assert queue.empty()

    e.emit(SubEventTwo())
    assert isinstance(await queue.get(), SubEventTwo)
    assert queue.empty()
