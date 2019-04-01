from contextlib import AbstractAsyncContextManager
from contextlib import asynccontextmanager
from functools import partial
from typing import *
import sys

import h11


class RenewableContextManager(AbstractAsyncContextManager):
    def __init__(self, factory, exceptions=(BaseException,)):
        self._factory = factory
        self._exceptions = exceptions
        self._context = None
        self._resource = None

    async def __aenter__(self):
        @asynccontextmanager
        async def renew_context():
            if self._resource is None:
                self._context = self._factory()
                self._resource = await self._context.__aenter__()

            try:
                yield self._resource
            except self._exceptions:
                try:
                    await self._context.__aexit__(*sys.exc_info())
                finally:
                    self._resource = None
                    self._context = None

        return renew_context

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self._context is not None:
            await self._context.__aexit__(exc_type, exc_value, traceback)

        return exc_type is None


def make_connection_manager(client_factory: Callable[[], AsyncContextManager[Any]]):
    """Convenience RenewableContextManager wrapper to make a context manager
    suitable for use as a connection manager.

    """

    return partial(
        RenewableContextManager,
        factory=client_factory,
        exceptions=(h11.RemoteProtocolError,)
    )
