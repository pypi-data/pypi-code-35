import unittest

from rover_position_rjg.data.flags import Flags
from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.filters.attitude_filter import AttitudeOutput, Data
from rover_position_rjg.position.position.dummy_position_algorithm import DummyPositionAlgorithm
from rover_position_rjg.position.position.position_input import PositionInput


class DummyPositionAlgorithmTest(unittest.TestCase):
    def test_returns_dummy_value(self):
        attitude = Quaternion.identity()
        acceleration = Vector.one()
        status = Flags(0xFF)
        ao = AttitudeOutput(acceleration, attitude, status)
        velocity = Vector.zero()
        position = Vector.zero()
        the_input = PositionInput(Data(ao, 1), Data(velocity, 2), Data(position, 3))
        algorithm = DummyPositionAlgorithm()
        # Act
        data = algorithm.step(the_input)
        # Assert
        self.assertEqual(attitude, data.attitude)
        self.assertEqual(acceleration, data.acceleration)
        self.assertEqual(Vector.one(), data.velocity)
        self.assertEqual(Vector.one(), data.position)
