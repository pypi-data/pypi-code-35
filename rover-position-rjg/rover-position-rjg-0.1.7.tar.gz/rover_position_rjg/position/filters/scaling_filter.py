from abc import ABC

from rover_position_rjg.data.data import TValue, Data
from rover_position_rjg.data.data_filter import DataFilter
from rover_position_rjg.position.calibration.scaler import Scaler


class ScalingFilter(DataFilter[TValue, TValue], ABC):
    """Scales a piece of data before passing it on"""

    def __init__(self, scaler: Scaler[TValue], name: str = ''):
        super().__init__(name)
        self._scaler = scaler

    def receive(self, data: Data[TValue]) -> None:
        scaled = self._scaler.scale(data)
        self.send(scaled)

