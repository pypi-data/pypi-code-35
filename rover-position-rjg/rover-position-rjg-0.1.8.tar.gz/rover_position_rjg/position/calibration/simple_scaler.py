from json import loads
from typing import TypeVar

from rover_position_rjg.data.data import Data
from rover_position_rjg.position.calibration.scaler import Scaler

TValue = TypeVar('TValue')


class SimpleScaler(Scaler[TValue]):
    """Scales a value with an offset and a multiplier."""
    offset = ...  # type: TValue
    multiplier = ...  # type: TValue

    def __init__(self, offset: TValue, multiplier: TValue):
        self.offset = offset
        self.multiplier = multiplier

    def scale(self, data: Data[TValue]) -> Data[TValue]:
        """Converts raw data into scaled and calibrated real values"""
        scaled_value = (data.value - self.offset).scale(self.multiplier)
        return Data(scaled_value, data.timestamp)

    def save(self, filename: str) -> None:
        data = '{{"offset":{}, "multiplier":{}}}'.format(self.offset.to_json(), self.multiplier.to_json())
        with open(filename, 'w') as writer:
            writer.write(data)

    def load(self, filename: str) -> None:
        with open(filename) as reader:
            data = reader.read()
        obj = loads(data)
        self.offset = self.offset.from_json(obj['offset'])
        self.multiplier = self.multiplier.from_json(obj['multiplier'])
