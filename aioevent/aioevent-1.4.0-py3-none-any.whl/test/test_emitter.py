import asyncio
import pytest

from aioevent import EventEmitter, BaseEvent


pytestmark = pytest.mark.asyncio


class ConnectionOpenedEvent(BaseEvent):
    pass


class ConnectionClosedEvent(BaseEvent):
    pass


class ConnectionMock(EventEmitter):
    def __init__(self, loop):
        super().__init__(loop=loop)
        self.status = "uninitialized"

    def open(self):
        self.status = "open"
        self.emit(ConnectionOpenedEvent())

    def close(self):
        self.status = "closed"
        self.emit(ConnectionClosedEvent())


async def test_basic(event_loop: "asyncio.AbstractEventLoop"):

    seen_opened = event_loop.create_future()
    seen_closed: "asyncio.Future" = event_loop.create_future()

    def on_open(event):
        assert isinstance(event, ConnectionOpenedEvent)
        nonlocal seen_opened
        seen_opened.set_result(True)

    async def on_close(event):
        assert isinstance(event, ConnectionClosedEvent)
        await asyncio.sleep(0.1)
        nonlocal seen_closed
        seen_closed.set_result(True)

    connection = ConnectionMock(event_loop)
    connection.listen(ConnectionOpenedEvent, on_open)
    connection.listen(ConnectionClosedEvent, on_close)

    connection.open()
    assert await asyncio.wait_for(seen_opened, 1) and not seen_closed.done()
    connection.close()
    assert await asyncio.wait_for(seen_closed, 1) and seen_closed.result()


async def test_broad_listener(event_loop: "asyncio.AbstractEventLoop"):
    events_seen_future: "asyncio.Future" = event_loop.create_future()

    def on_event(event):
        nonlocal events_seen_future
        events_seen_future.set_result(True)

    connection = ConnectionMock(event_loop)
    connection.listen(BaseEvent, on_event)

    connection.open()
    assert await asyncio.wait_for(events_seen_future, 1)

    # reset future
    events_seen_future = event_loop.create_future()
    connection.close()
    assert await asyncio.wait_for(events_seen_future, 1)
