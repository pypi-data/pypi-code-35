from typing import Dict

from aiobinance.modules.base import BaseModule
from aiobinance.types import ApiVersion


class Stream(BaseModule):
    """Start a new user data stream. The stream will close after 60 minutes unless a keepalive is sent.

    https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#user-data-stream-endpoints
    """

    async def start(self) -> Dict:
        """Start a new user data stream. The stream will close after 60 minutes unless a keepalive is sent.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#start-user-data-stream-user_stream
        """
        return await self._post('userDataStream', version=ApiVersion.V1)

    async def keepalive(self, listen_key: str) -> Dict:
        """Keepalive a user data stream to prevent a time out. User data streams will close after 60 minutes. It's recommended to send a ping about every 30 minutes.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#keepalive-user-data-stream-user_stream
        """
        return await self._put('userDataStream', params={'listenKey': listen_key}, version=ApiVersion.V1)

    async def close(self, listen_key: str) -> Dict:
        """Close out a user data stream.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#close-user-data-stream-user_stream
        """
        return await self._delete('userDataStream', params={'listenKey': listen_key}, version=ApiVersion.V1)
