import struct

from rover_position_rjg.position.filters.attitude_filter import AttitudeOutput
from rover_position_rjg.data.data import Data
from rover_position_rjg.data.data_filter import DataFilter


class AttitudeToHeadingBytesFilter(DataFilter[AttitudeOutput, bytes]):
    def __init__(self, name: str = ''):
        super().__init__(name)

    def receive(self, data: Data[AttitudeOutput]) -> None:
        a = data.value.attitude.to_tait_bryan()
        packed = struct.pack(">fffBf", a.x, a.y, a.z, int(data.value.status), float(data.timestamp) / 1e9)
        self.send(Data(packed, data.timestamp))
