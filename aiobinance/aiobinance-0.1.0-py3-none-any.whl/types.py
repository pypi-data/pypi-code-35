from enum import Enum


class ApiVersion(Enum):
    V1 = 'v1'
    V3 = 'v3'


class HttpMethod(Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'


class OrderSide(Enum):
    BUY = 'buy'
    SELL = 'sell'


class OrderType(Enum):
    LIMIT = 'LIMIT'
    MARKET = 'MARKET'
    STOP_LOSS = 'STOP_LOSS'
    STOP_LOSS_LIMIT = 'STOP_LOSS_LIMIT'
    TAKE_PROFIT = 'TAKE_PROFIT'
    TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'
    LIMIT_MAKER = 'LIMIT_MAKER'


class Interval(Enum):
    MIN1 = '1m'
    MIN3 = '3m'
    MIN5 = '5m'
    MIN15 = '15m'
    MIN30 = '30m'
    HOUR1 = '1h'
    HOUR2 = '2h'
    HOUR4 = '4h'
    HOUR6 = '6h'
    HOUR8 = '8h'
    HOUR12 = '12h'
    DAY1 = '1d'
    DAY3 = '3d'
    WEEK1 = '1w'
    MONTH1 = '1M'


class TimeInForce(Enum):
    GTC = 'GTC'  # Good Till Cancelled
    IOC = 'IOC'  # Fill Or Kill
    FOK = 'FOK'  # Immediate Or Cancel


class OrderResponseType(Enum):
    ACK = 'ACK'
    RESULT = 'RESULT'
    FULL = 'FULL'
