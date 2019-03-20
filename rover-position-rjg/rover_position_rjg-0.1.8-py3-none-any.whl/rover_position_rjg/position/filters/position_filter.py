from abc import ABC

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.data_filter import DataFilter
from rover_position_rjg.position.position.position import Position

from rover_position_rjg.position.position.position_algorithm import PositionAlgorithm
from rover_position_rjg.position.position.position_input import PositionInput


class PositionFilter(DataFilter[PositionInput, Position], ABC):
    """Uses some algorithm to determine the current position,
    velocity and acceleration of the rover."""

    def __init__(self, algorithm: PositionAlgorithm, name: str = ''):
        super().__init__(name)
        self.algorithm = algorithm

    def receive(self, data: Data[PositionInput]) -> None:
        output = self.algorithm.step(data.value)
        self.send(Data(output, data.timestamp))
