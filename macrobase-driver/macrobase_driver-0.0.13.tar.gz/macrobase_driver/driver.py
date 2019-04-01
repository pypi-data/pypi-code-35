from asyncio import AbstractEventLoop, get_event_loop
from typing import ClassVar

from macrobase_driver.context import Context
from macrobase_driver.config import DriverConfig
from macrobase_driver.hook import HookNames, HookHandler


class MacrobaseDriver(object):

    def __init__(self, name: str = None, *args, **kwargs):
        self.name = name
        self.config = DriverConfig
        self.context = Context()

    @property
    def loop(self) -> AbstractEventLoop:
        return get_event_loop()

    def update_config(self, config_obj: ClassVar[DriverConfig]):
        pass

    def add_hook(self, name: HookNames, handler):
        pass

    async def _call_hooks(self, name: HookNames):
        if name not in self._hooks:
            return

        for handler in self._hooks[name]:
            await handler(self, self.loop)

    def run(self, *args, **kwargs):
        pass
