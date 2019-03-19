from rover_position_rjg.data.data import Data
from rover_position_rjg.data.data_filter import DataFilter
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.position.position_input import PositionInput


class DecawaveToPositionInputFilter(DataFilter[Vector, PositionInput]):
    def __init__(self):
        super().__init__()

    def receive(self, data: Data[Vector]) -> None:
        position_input = PositionInput(position=data)
        self.send(Data(position_input, data.timestamp))
