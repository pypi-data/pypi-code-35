from abc import *

from rover_position_rjg.position.position.position import Position
from rover_position_rjg.position.position.position_input import PositionInput


class PositionAlgorithm(ABC):
    """A step wise algorithm for determining the rover's position
    speed and acceleration from various inputs. e.g. a Kalman filter"""

    @abstractmethod
    def step(self, data: PositionInput) -> Position:
        pass
