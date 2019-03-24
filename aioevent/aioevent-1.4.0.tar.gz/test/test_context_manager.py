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


async def test_subscription_context_manager():
    emitter = EventEmitter()
    payload_queue = asyncio.Queue()

    @event_listener(emitter, PayloadEvent)
    def on_payload_event(event: "PayloadEvent"):
        print("Got payload event:", event.payload)
        payload_queue.put_nowait(event.payload)

    with on_payload_event:
        emitter.emit(PayloadEvent("one"))
        emitter.emit(PayloadEvent("two"))
    emitter.emit(PayloadEvent("three"))

    assert (await payload_queue.get()) == "one"
    assert (await payload_queue.get()) == "two"
    assert payload_queue.empty()
