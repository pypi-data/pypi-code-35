import asyncio
from asyncio import AbstractEventLoop

loop = asyncio.get_event_loop()


def get_loop() -> AbstractEventLoop:
    if not loop or not loop.is_running():
        asyncio.set_event_loop(asyncio.new_event_loop())
    return asyncio.get_event_loop()
