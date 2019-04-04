from .ticker import Pair
from .common import Value, Parameter, Interval


class Open():
    pass


class High():
    pass


class Low():
    pass


class Close(Value):
    def __init__(
        self,
        pair: Pair = Parameter('pair'),
        interval: Interval = Parameter('interval'),
        shift: int = 0
    ):
        super().__init__(
            key='close_%s_%s_%s' % (pair.get_key(), interval, shift))
