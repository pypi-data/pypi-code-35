from decimal import Decimal
from enum import Enum

from .ticker import Symbol
from .volume import Volume
from .common import Instructions, Instruction


class Side(Enum):
    BUY = 'buy'
    SELL = 'sell'


class placeOrder(Instruction):
    def __init__(self):
        Instructions().add(self)


class placeLimitOrder(placeOrder):
    def __init__(
        self, symbol: Symbol, side: Side, volume: Volume, price: Decimal
    ):
        pass


class placeMarketOrder(placeOrder):
    def __init__(self, symbol: Symbol, side: Side, volume: Volume):
        super().__init__()


class placeMakerOrder(placeOrder):
    def __init__(self, symbol: Symbol, side: Side, volume: Volume):
        pass


class placeTakerOrder(placeOrder):
    def __init__(self, symbol: Symbol, side: Side, volume: Volume):
        pass
