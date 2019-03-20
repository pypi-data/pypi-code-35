from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector


class Position:
    """The attitude and position of a device in a frame of reference.
    Usually the world frame of reference."""
    def __init__(self,
                 attitude: Quaternion,
                 acceleration: Vector,
                 velocity: Vector,
                 position: Vector
                 ):
        self.attitude = attitude
        self.acceleration = acceleration
        self.velocity = velocity
        self.position = position
