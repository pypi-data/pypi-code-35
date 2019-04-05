from decimal import Decimal
from typing import Union

from aiobinance.modules.base import BaseModule
from aiobinance.types import OrderSide, OrderType, TimeInForce, OrderResponseType, ApiVersion
from aiobinance.utils import check_limit_max, check_mandatory_params


class Account(BaseModule):
    """Account endpoints

    https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#account-endpoints
    """

    async def new_order(
            self,
            symbol: str,
            side: OrderSide,
            order_type: OrderType,
            quantity: Union[Decimal, int, str],
            time_in_force: TimeInForce,
            price: Union[Decimal, int, str],
            new_client_order_id: str = None,
            stop_price: Union[Decimal, int, str] = None,
            iceberq_qty: Union[Decimal, int, str] = None,
            new_order_resp_type: OrderResponseType = None,
            recv_window: int = None,
            test: bool = False
    ):
        """Send in a new order.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#new-order--trade
        """
        check_mandatory_params(**locals())
        if iceberq_qty is not None and TimeInForce(time_in_force) != TimeInForce.GTC:
            raise ValueError('Any order with an icebergQty MUST have timeInForce set to GTC.')

        return await self._post(
            'order/test' if test else 'order',
            params={
                'symbol': symbol,
                'side': OrderSide(side),
                'type': OrderType(order_type),
                'timeInForce': TimeInForce(time_in_force),
                'quantity': quantity,
                'price': price,
                'newClientOrderId': new_client_order_id,
                'stopPrice': stop_price,
                'icebergQty': iceberq_qty,
                'newOrderRespType': new_order_resp_type,
                'recvWindow': recv_window,
            },
            version=ApiVersion.V3
        )

    async def get_order(
            self,
            symbol: str,
            order_id: int = None,
            orig_client_order_id: str = None,
            recv_window: int = None,
    ):
        """Check an order's status.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#query-order-user_data
        """
        if order_id is None and orig_client_order_id is None:
            raise ValueError('Either orderId or origClientOrderId must be sent.')

        return await self._get(
            'order',
            sign=True,
            params={
                'symbol': symbol,
                'orderId': order_id,
                'origClientOrderId': orig_client_order_id,
                'recvWindow': recv_window,
            },
            version=ApiVersion.V3
        )

    async def cancel_order(
            self,
            symbol: str,
            order_id: int = None,
            orig_client_order_id: str = None,
            new_client_order_id: str = None,
            recv_window: int = None,
    ):
        """Cancel an active order.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#cancel-order-trade
        """
        if order_id is None and orig_client_order_id is None:
            raise ValueError('Either orderId or origClientOrderId must be sent.')

        return await self._delete(
            'order',
            sign=True,
            params={
                'symbol': symbol,
                'orderId': order_id,
                'origClientOrderId': orig_client_order_id,
                'newClientOrderId': new_client_order_id,
                'recvWindow': recv_window,
            },
            version=ApiVersion.V3
        )

    async def open_orders(
            self,
            symbol: str = None,
            recv_window: int = None,
    ):
        """Get all open orders on a symbol. Careful when accessing this with no symbol.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#current-open-orders-user_data
        """
        return await self._get(
            'openOrders',
            sign=True,
            params={
                'symbol': symbol,
                'recvWindow': recv_window,
            },
            version=ApiVersion.V3
        )

    async def all_orders(
            self,
            symbol: str,
            order_id: int = None,
            start_time: int = None,
            end_time: int = None,
            limit: int = None,
            recv_window: int = None,
    ):
        """Get all account orders; active, canceled, or filled.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#all-orders-user_data
        """
        return await self._get(
            'allOrders',
            sign=True,
            params={
                'symbol': symbol,
                'orderId': order_id,
                'startTime': start_time,
                'endTime': end_time,
                'limit': check_limit_max(limit),
                'recvWindow': recv_window,
            },
            version=ApiVersion.V3
        )

    async def info(
            self,
            recv_window: int = None,
    ):
        """Get current account information.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#account-information-user_data
        """
        return await self._get(
            'account',
            sign=True,
            params={
                'recvWindow': recv_window,
            },
            version=ApiVersion.V3
        )

    async def trades(
            self,
            symbol: str,
            start_time: int = None,
            end_time: int = None,
            from_id: int = None,
            limit: int = None,
            recv_window: int = None,
    ):
        """Get trades for a specific account and symbol.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#account-trade-list-user_data
        """
        return await self._get(
            'myTrades',
            sign=True,
            params={
                'symbol': symbol,
                'fromId': from_id,
                'startTime': start_time,
                'endTime': end_time,
                'limit': check_limit_max(limit),
                'recvWindow': recv_window,
            },
            version=ApiVersion.V3
        )
