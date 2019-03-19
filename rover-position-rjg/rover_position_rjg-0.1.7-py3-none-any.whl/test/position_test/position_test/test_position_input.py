import unittest

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.flags import Flags
from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.filters.attitude_filter import AttitudeOutput
from rover_position_rjg.position.position.position_input import PositionInput


class PositionInputTest(unittest.TestCase):
    def test_constructor(self):
        attitude = Quaternion.identity()
        acceleration = Vector.zero()
        status = Flags(0x12)
        ao = AttitudeOutput(acceleration, attitude, status)
        velocity = Vector.zero()
        position = Vector.zero()
        # Act
        sut = PositionInput(Data(ao, 1), Data(velocity, 2), Data(position, 3))
        # Assert
        self.assertEqual(1, sut.attitude.timestamp)
        self.assertEqual(attitude, sut.attitude.value.attitude)
        self.assertEqual(acceleration, sut.attitude.value.acceleration)
        self.assertEqual(status, sut.attitude.value.status)
        self.assertEqual(2, sut.velocity.timestamp)
        self.assertEqual(velocity, sut.velocity.value)
        self.assertEqual(3, sut.position.timestamp)
        self.assertEqual(position, sut.position.value)

    def test_constructor_must_have_an_argument(self):
        with self.assertRaisesRegex(RuntimeError, 'PositionInput must contain at least one value'):
            sut = PositionInput()

