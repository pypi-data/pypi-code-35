import unittest

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.attitude.attitude_algorithm import AttitudeAlgorithm
from rover_position_rjg.position.attitude.modified_madgwick import ModifiedMadgwick
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class ModifiedMadgwickTest(unittest.TestCase):
    def test_not_initialised_by_default(self):
        a = ModifiedMadgwick()
        self.assertFalse(a.initialised)

    def test_initialise_sets_attitude_estimate(self):
        a = ModifiedMadgwick()
        data = self.build_data(Vector([0, 1, 0]), Vector.zero(), Vector([0, -0.43, -0.20]), 100)
        a.step(data)  # Take an initial step so algorithm isn't in its original state
        tait_bryan_angles = Vector([20, 30, -90])
        attitude = Quaternion.from_tait_bryan(tait_bryan_angles)
        # Act
        a.initialise(attitude, 123)
        # Assert
        self.assertTrue(a.initialised)
        self.assertNotEqual(1, a.q0)
        self.assertNotEqual(0, a.q1)
        self.assertNotEqual(0, a.q2)
        self.assertNotEqual(0, a.q3)

    def test_initialise_sets_timestamp(self):
        a = ModifiedMadgwick()
        data = self.build_data(Vector([0, 1, 0]), Vector.zero(), Vector([0, -0.43, -0.20]), 100)
        a.step(data)  # Take an initial step so algorithm isn't in its original state
        tait_bryan_angles = Vector([20, 30, -90])
        attitude = Quaternion.from_tait_bryan(tait_bryan_angles)
        # Act
        a.initialise(attitude, 123)
        # Assert
        self.assertEqual(123, a.previous_timestamp)

    def test_initialises_itself_from_first_data(self):
        a = ModifiedMadgwick()
        data = self.build_data(Vector([0, 1, 0]), Vector.zero(), Vector([0, -0.43, -0.20]), 100)
        q = a.step(data)
        self.assertEqual(q, AttitudeAlgorithm.quaternion_from_imu(data))
        self.assertEqual(data.angular_velocity.timestamp, a.previous_timestamp)
        self.assertTrue(a.initialised)

    def test_does_not_reinitialise_from_data_after_call_to_initialise(self):
        a = ModifiedMadgwick()
        tait_bryan_angles = Vector([20, 30, -90])
        attitude = Quaternion.from_tait_bryan(tait_bryan_angles)
        a.initialise(attitude, 123)
        # Act
        data = self.build_data(Vector([0, 1, 0]), Vector.zero(), Vector([0, -0.43, -0.20]), 100)
        q = a.step(data)
        # Assert
        self.assertNotEqual(q, AttitudeAlgorithm.quaternion_from_imu(data))

    def test_reset_sets_algorithm_to_uninitialised_state(self):
        a = ModifiedMadgwick()
        data = self.build_data(Vector([0, 1, 0]), Vector.zero(), Vector([0, -0.43, -0.20]), 100)
        a.step(data)  # Take an initial step to algorithm isn't in its original state
        # Act
        a.reset()
        # Assert
        self.assertFalse(a.initialised)
        self.assertEqual(0, a.previous_timestamp)
        self.assertEqual(1, a.q0)
        self.assertEqual(0, a.q1)
        self.assertEqual(0, a.q2)
        self.assertEqual(0, a.q3)

    @staticmethod
    def build_data(acc: Vector, gyro: Vector, mag: Vector, timestamp: float) -> NineDoFData:
        return NineDoFData(Data(acc, timestamp-1), Data(gyro, timestamp), Data(mag, timestamp+1), Data(22, timestamp+2))
