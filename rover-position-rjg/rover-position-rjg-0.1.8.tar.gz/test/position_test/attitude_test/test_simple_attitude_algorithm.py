import math
import unittest

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.attitude.attitude_algorithm import AttitudeAlgorithm
from rover_position_rjg.position.attitude.simple_attitude_algorithm import SimpleAttitudeAlgorithm
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class SimpleAttitudeAlgorithmTest(unittest.TestCase):
    def test_not_initialised_by_default(self):
        a = SimpleAttitudeAlgorithm()
        self.assertFalse(a.initialised)

    def test_initialise_sets_attitude_estimate(self):
        a = SimpleAttitudeAlgorithm()
        data = self.build_data(Vector([0, 1, 0]), Vector.zero(), Vector([0, -0.43, -0.20]), 100)
        a.step(data)  # Take an initial step to algorithm isn't in its original state
        tait_bryan_angles = Vector([20, 30, -90])
        attitude = Quaternion.from_tait_bryan(tait_bryan_angles)
        # Act
        a.initialise(attitude, 123)
        # Assert
        self.assertTrue(a.initialised)
        self.assertEqual(attitude, a.attitude)
        self.assertEqual(123, a.previous_timestamp)

    def test_initialises_itself_from_first_data(self):
        a = SimpleAttitudeAlgorithm()
        data = self.build_data(Vector([0, 1, 0]), Vector.zero(), Vector([0, -0.43, -0.20]), 100)
        q = a.step(data)
        self.assertEqual(q, AttitudeAlgorithm.quaternion_from_imu(data))
        self.assertEqual(data.angular_velocity.timestamp, a.previous_timestamp)
        self.assertTrue(a.initialised)

    def test_does_not_reinitialise_from_data_after_call_to_initialise(self):
        a = SimpleAttitudeAlgorithm()
        tait_bryan_angles = Vector([20, 30, -90])
        attitude = Quaternion.from_tait_bryan(tait_bryan_angles)
        a.initialise(attitude, 123)
        # Act
        data = self.build_data(Vector([0, 1, 0]), Vector.zero(), Vector([0, -0.43, -0.20]), 100)
        q = a.step(data)
        # Assert
        self.assertNotEqual(q, AttitudeAlgorithm.quaternion_from_imu(data))

    def test_integrates_gyro_only(self):
        acc = Vector([0, 1, 0])
        mag = Vector([0, -0.43, -0.20])
        a = SimpleAttitudeAlgorithm()
        data = self.build_data(acc, Vector([0, 0, 0]), mag, 100)
        q0 = a.step(data)
        # Act
        data = self.build_data(acc, Vector([math.radians(3), math.radians(2), math.radians(1)]), mag, 100.5)
        q1 = a.step(data)
        # Assert
        angles0 = q0.to_tait_bryan()
        angles1 = q1.to_tait_bryan()
        self.assertEqual(Vector([1.491274, -0.499924, 1.000038]), angles1 - angles0)

    def test_update_previous_timestamp(self):
        acc = Vector([0, 1, 0])
        mag = Vector([0, -0.43, -0.20])
        gyro = Vector.zero()
        a = SimpleAttitudeAlgorithm()
        data = self.build_data(acc, gyro, mag, 100)
        a.step(data)
        # Act
        data = self.build_data(acc, gyro, mag, 100.5)
        a.step(data)
        # Assert
        self.assertEqual(100.5, a.previous_timestamp)

    def test_reset_sets_algorithm_to_initial_state(self):
        a = SimpleAttitudeAlgorithm()
        data = self.build_data(Vector([0, 1, 0]), Vector.zero(), Vector([0, -0.43, -0.20]), 100)
        a.step(data)  # Take an initial step to algorithm isn't in its original state
        # Act
        a.reset()
        # Assert
        self.assertFalse(a.initialised)
        self.assertEqual(Vector.zero(), a.attitude)
        self.assertEqual(0, a.previous_timestamp)

    @staticmethod
    def build_data(acc: Vector, gyro: Vector, mag: Vector, timestamp: float) -> NineDoFData:
        return NineDoFData(Data(acc, timestamp-1), Data(gyro, timestamp), Data(mag, timestamp+1), Data(22, timestamp+2))
