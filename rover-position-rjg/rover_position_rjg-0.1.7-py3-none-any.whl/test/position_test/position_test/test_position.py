import unittest

from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.position.position import Position


class PositionTest(unittest.TestCase):
    def test_constructor(self):
        attitude = Quaternion.identity()
        acceleration = Vector.zero()
        velocity = Vector.zero()
        position = Vector.zero()
        # Act
        sut = Position(attitude, acceleration, velocity, position)
        # Assert
        self.assertEqual(attitude, sut.attitude)
        self.assertEqual(acceleration, sut.acceleration)
        self.assertEqual(velocity, sut.velocity)
        self.assertEqual(position, sut.position)
