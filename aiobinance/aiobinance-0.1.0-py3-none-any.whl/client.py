from asyncio import AbstractEventLoop

from aiobinance.modules.account import Account
from aiobinance.modules.general import General
from aiobinance.modules.market import Market
from aiobinance.modules.stream import Stream
from aiobinance.network import Network


class Client:
    def __init__(self, api_key: str, api_secret: str, loop: AbstractEventLoop = None, timeout: int = None) -> None:
        self._http = Network(api_key, api_secret, loop, timeout)

        self.account = Account(self._http)
        self.general = General(self._http)
        self.market = Market(self._http)
        self.stream = Stream(self._http)

    async def close(self):
        await self._http.close()
