from typing import Dict

from aiobinance.modules.base import BaseModule


class General(BaseModule):
    """General endpoints

    https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#general-endpoints
    """

    async def ping(self) -> Dict:
        """Test connectivity to the Rest API.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#test-connectivity
        """
        return await self._get('ping')

    async def time(self) -> Dict[str, int]:
        """Test connectivity to the Rest API and get the current server time.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#check-server-time
        """
        return await self._get('time')

    async def exchange_info(self) -> Dict:
        """Current exchange trading rules and symbol information.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#exchange-information
        """
        return await self._get('exchangeInfo')
