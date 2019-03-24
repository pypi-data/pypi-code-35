import asyncio
import pytest

from aioevent import EventEmitter, BaseEvent


pytestmark = pytest.mark.asyncio


class ChildEvent(BaseEvent):
    pass


class ParentEvent(BaseEvent):
    pass


class Child(EventEmitter):
    def trigger_event(self):
        self.emit(ChildEvent())


class Parent(EventEmitter):
    def __init__(self, loop):
        super().__init__(loop=loop)
        self.child = Child(loop=loop)
        self.proxy(self.child)

    def trigger_event(self):
        self.emit(ParentEvent())


class GrandParent(EventEmitter):
    def __init__(self, loop):
        super().__init__(loop=loop)
        self.child = Parent(loop=loop)
        self.proxy(self.child)


async def test_child_proxy(event_loop: "asyncio.AbstractEventLoop"):
    child_event_future: "asyncio.Future" = event_loop.create_future()

    async def event_handler(event: BaseEvent):
        assert isinstance(event, ChildEvent)
        child_event_future.set_result(True)

    parent = Parent(event_loop)
    parent.listen(ChildEvent, event_handler)
    parent.child.trigger_event()

    assert await asyncio.wait_for(child_event_future, 1)


async def test_nested_listeners(event_loop: "asyncio.AbstractEventLoop"):
    parent_event_future: "asyncio.Future" = event_loop.create_future()
    child_event_future: "asyncio.Future" = event_loop.create_future()

    async def parent_event_handler(event: BaseEvent):
        assert isinstance(event, ChildEvent)
        parent_event_future.set_result(True)

    async def child_event_handler(event: BaseEvent):
        assert isinstance(event, ChildEvent)
        child_event_future.set_result(True)

    parent = Parent(event_loop)
    parent.child.listen(ChildEvent, child_event_handler)
    parent.listen(ChildEvent, parent_event_handler)
    parent.child.trigger_event()

    assert await asyncio.wait_for(child_event_future, 1)
    assert await asyncio.wait_for(parent_event_future, 1)
