from json import loads
from rover_position_rjg.data.data import Data
from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.calibration.scaler import Scaler


class RotationScaler(Scaler[Vector]):
    """Rotates the input vector"""
    def __init__(self, rotation: Quaternion):
        self._rotation = rotation

    def scale(self, data: Data[Vector]) -> Data[Vector]:
        """Rotates the input vector"""
        scaled_value = self._rotation.rotate(data.value)
        return Data(scaled_value, data.timestamp)

    def save(self, filename: str) -> None:
        data = '{{"rotation":{}}}'.format(self._rotation.to_json())
        with open(filename, 'w') as writer:
            writer.write(data)

    def load(self, filename: str) -> None:
        with open(filename) as reader:
            data = reader.read()
        obj = loads(data)
        quaternion = obj['rotation']
        self._rotation = Quaternion.from_json(quaternion)
