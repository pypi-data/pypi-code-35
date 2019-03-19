from rover_position_rjg.data.data import Data
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.filters.attitude_filter import AttitudeOutput


class PositionInput:
    def __init__(self,
                 attitude: Data[AttitudeOutput] = None,
                 velocity: Data[Vector] = None,
                 position: Data[Vector] = None
                 ):
        """All arguments are optional but at least one must be provided."""
        self.attitude = attitude
        self.velocity = velocity
        self.position = position
        if self.attitude is None and self.velocity is None and self.position is None:
            raise RuntimeError('PositionInput must contain at least one value')
