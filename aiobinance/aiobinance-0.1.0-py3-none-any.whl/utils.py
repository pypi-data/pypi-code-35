from typing import Dict, Tuple, Optional

from aiobinance.types import OrderType


def check_limit_max(limit: Optional[int], limit_max: int = 1000) -> int:
    if limit and limit > limit_max:
        raise ValueError(f'Invalid limit. Limit max: {limit_max}')
    return limit


def check_mandatory_params(**params: Dict):
    order_type: OrderType = OrderType(params['order_type'])
    mandatory_params = {
        OrderType.LIMIT: ('time_in_force', 'quantity', 'price',),
        OrderType.MARKET: ('quantity',),
        OrderType.STOP_LOSS: ('quantity', 'stop_price'),
        OrderType.STOP_LOSS_LIMIT: ('time_in_force', 'quantity', 'price', 'stop_price'),
        OrderType.TAKE_PROFIT: ('quantity', 'stop_price'),
        OrderType.TAKE_PROFIT_LIMIT: ('time_in_force', 'quantity', 'price', 'stop_price'),
        OrderType.LIMIT_MAKER: ('quantity', 'stop_price'),
    }.get(order_type)

    for param in mandatory_params:
        if params.get(param) is None:
            raise ValueError(f'Mandatory parameters for the order type {order_type.value}: {mandatory_params}')


def check_limit_values(limit: int, valid_limits: Tuple[int, ...] = (5, 10, 20, 50, 100, 500, 1000)) -> int:
    if limit not in valid_limits:
        raise ValueError(f'Invalid limit. Valid limits: {valid_limits}')
    return limit
