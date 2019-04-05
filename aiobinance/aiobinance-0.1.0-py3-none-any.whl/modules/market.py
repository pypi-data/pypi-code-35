from typing import Dict, List, Any, Union

from aiobinance.modules.base import BaseModule
from aiobinance.types import Interval, ApiVersion
from aiobinance.utils import check_limit_max, check_limit_values


class Market(BaseModule):
    """Market Data endpoints

    https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#market-data-endpoints
    """

    async def order_book(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        """Order book

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#order-book
        """

        return await self._get(
            'depth',
            params={
                'symbol': symbol,
                'limit': check_limit_values(limit)
            }
        )

    async def recent_trades(self, symbol: str, limit: int = None) -> List[Dict[str, Any]]:
        """Get recent trades (up to last 500).

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#recent-trades-list
        """
        return await self._get(
            'trades',
            params={
                'symbol': symbol,
                'limit': check_limit_max(limit)
            }
        )

    async def historical_trades(self, symbol: str, limit: int = None, from_id: int = None) -> List[Dict[str, Any]]:
        """Get older trades.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#old-trade-lookup-market_data
        """
        return await self._get(
            'historicalTrades',
            params={
                'symbol': symbol,
                'limit': check_limit_max(limit),
                'fromId': from_id
            }
        )

    async def agg_trades(
            self,
            symbol: str,
            from_id: int = None,
            start_time: int = None,
            end_time: int = None,
            limit: int = None
    ) -> Dict:
        """Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same price will have the quantity aggregated.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#compressedaggregate-trades-list
        """
        return await self._get(
            'historicalTrades',
            params={
                'symbol': symbol,
                'fromId': from_id,
                'startTime': start_time,
                'endTime': end_time,
                'limit': check_limit_max(limit),
            }
        )

    async def klines(
            self,
            symbol: str,
            interval: Interval,
            start_time: int = None,
            end_time: int = None,
            limit: int = None
    ) -> List[List]:
        """Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#klinecandlestick-data
        """
        return await self._get(
            'klines',
            params={
                'symbol': symbol,
                'interval': Interval(interval).value,
                'startTime': start_time,
                'endTime': end_time,
                'limit': limit,
            }
        )

    async def avg_price(self, symbol: str) -> Dict[str, Any]:
        """Current average price for a symbol.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#current-average-price
        """

        return await self._get(
            'avgPrice',
            params={
                'symbol': symbol,
            },
            version=ApiVersion.V3
        )

    async def ticker_24hr(self, symbol: str = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """24 hour rolling window price change statistics. Careful when accessing this with no symbol.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#current-average-price
        """

        return await self._get(
            'ticker/24hr',
            params={
                'symbol': symbol,
            }
        )

    async def ticker_price(self, symbol: str = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Latest price for a symbol or symbols.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#symbol-price-ticker
        """

        return await self._get(
            'ticker/price',
            params={
                'symbol': symbol,
            }
        )
