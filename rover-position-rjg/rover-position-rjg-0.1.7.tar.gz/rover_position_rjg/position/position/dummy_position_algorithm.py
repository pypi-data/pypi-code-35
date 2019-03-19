from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.position.position import Position
from rover_position_rjg.position.position.position_algorithm import PositionAlgorithm, ABC
from rover_position_rjg.position.position.position_input import PositionInput


class DummyPositionAlgorithm(PositionAlgorithm, ABC):
    def __init__(self):
        super().__init__()

    def step(self, data: PositionInput) -> Position:
        return Position(
            data.attitude.value.attitude,
            data.attitude.value.acceleration,
            Vector.one(),
            Vector.one())
