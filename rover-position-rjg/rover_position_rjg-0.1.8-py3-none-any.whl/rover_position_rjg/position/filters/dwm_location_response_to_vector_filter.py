from decawave_1001_rjg import DwmLocationResponse

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.data_filter import DataFilter
from rover_position_rjg.data.vector import Vector


class DwmLocationResponseToVectorFilter(DataFilter[DwmLocationResponse, Vector]):
    def __init__(self, name: str = ''):
        super().__init__(name)
        self.to_metres = Vector([0.001, 0.001, 0.001])
    
    def receive(self, data: Data[DwmLocationResponse]) -> None:
        unscaled_position = Vector(data.value.get_tag_position().position())
        position = unscaled_position.scale(self.to_metres)
        self.send(Data(position, data.timestamp))
