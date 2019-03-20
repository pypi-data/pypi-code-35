from rover_position_rjg.data.data import Data
from rover_position_rjg.data.data_filter import DataFilter, TValue


class FanOutFilter(DataFilter[TValue, TValue]):
    """A filter that simply passes incoming data to its receivers."""

    def __init__(self):
        super().__init__()

    def receive(self, data: Data[TValue]) -> None:
        self.send(data)
