import asyncio
from typing import TYPE_CHECKING, NamedTuple
import pytest
from aioevent import EventEmitter, BaseEvent, event_listener

if TYPE_CHECKING:
    from asyncio.events import AbstractEventLoop


pytestmark = pytest.mark.asyncio


class PayloadEvent(BaseEvent):
    def __init__(self, payload):
        super().__init__()
        self.payload = payload
    payload: str


async def test_sync_decorator_listens():
    emitter = EventEmitter()
    payload_queue = asyncio.Queue()

    @event_listener(emitter, PayloadEvent)
    def on_payload_event(event: "PayloadEvent"):
        print("Got payload event:", event.payload)
        payload_queue.put_nowait(event.payload)

    emitter.emit(PayloadEvent("one"))
    emitter.emit(PayloadEvent("two"))
    on_payload_event.unsubscribe()
    emitter.emit(PayloadEvent("three"))

    assert (await payload_queue.get()) == "one"
    assert (await payload_queue.get()) == "two"
    assert payload_queue.empty()


async def test_async_decorator_listens(event_loop: "AbstractEventLoop"):
    emitter = EventEmitter()
    payload_future = event_loop.create_future()

    @event_listener(emitter, PayloadEvent)
    async def on_payload_event(event: "PayloadEvent"):
        print("Got payload event:", event.payload)
        payload_future.set_result(event.payload)

    emitter.emit(PayloadEvent("foo!"))
    assert (await payload_future) == "foo!"
