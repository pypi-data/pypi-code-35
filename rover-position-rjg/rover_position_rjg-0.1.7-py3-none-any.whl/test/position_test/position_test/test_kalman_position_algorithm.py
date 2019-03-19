import math
import numpy as np
import unittest

from rover_position_rjg.data.flags import Flags
from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.filters.attitude_filter import AttitudeOutput, Data
from rover_position_rjg.position.position.kalman_position_algorithm import KalmanPositionAlgorithm
from rover_position_rjg.position.position.position_input import PositionInput


class FakeKalman:
    def __init__(self, state: np.ndarray):
        self.state = state


class KalmanPositionAlgorithmTest(unittest.TestCase):
    def test_kalman_starts_at_position_0(self):
        kpa = KalmanPositionAlgorithm(100, 0.1, 0.2, 0.01)
        x0 = np.array([[0], [0], [0], [0], [0], [0], [0], [0], [0]])
        self.assertTrue(np.array_equal(x0, kpa.kalman.x))

    def test_first_position_sets_position_directly(self):
        # Arrange
        kpa = KalmanPositionAlgorithm(100, 0.01, 0.2, 0.01)
        actual_position = Vector([0.1, 0.2, 0.3])
        # Act
        position = kpa.step(PositionInput(position=Data(actual_position, 123.00)))
        # Assert
        self.assertIsNone(position.attitude)
        self.assertEqual(Vector.zero(), position.acceleration)
        self.assertEqual(Vector.zero(), position.velocity)
        self.assertVectorAlmostEqual(actual_position, position.position)

    def test_first_velocity_sets_velocity_directly(self):
        # Arrange
        kpa = KalmanPositionAlgorithm(100, 0.1, 0.001, 0.01)
        velocity = Vector([0.1, 0.2, 0.3])
        # Act
        position = kpa.step(PositionInput(velocity=Data(velocity, 123.00)))
        # Assert
        self.assertIsNone(position.attitude)
        self.assertEqual(Vector.zero(), position.acceleration)
        self.assertVectorAlmostEqual(velocity, position.velocity)
        self.assertVectorAlmostEqual(Vector([0.0010, 0.0020, 0.0030]), position.position)

    def test_first_acceleration_sets_acceleration_directly(self):
        # Arrange
        kpa = KalmanPositionAlgorithm(100, 0.1, 0.2, 0.01)
        ao = AttitudeOutput(Vector([1, 2, 3]), Quaternion.identity(), Flags())
        # Act. Need 2 steps to get moving
        position = kpa.step(PositionInput(Data(ao, 123.00)))
        position = kpa.step(PositionInput(Data(ao, 123.01)))
        # Assert
        self.assertEqual(ao.attitude, position.attitude)
        self.assertVectorAlmostEqual(Vector([1, 2, 3]), position.acceleration)
        self.assertVectorAlmostEqual(Vector([0.01, 0.02, 0.03]), position.velocity)
        self.assertVectorAlmostEqual(Vector([0.00005, 0.0001, 0.00015]), position.position)

    def test_can_update_kalman_with_position_only(self):
        # Arrange
        kpa = KalmanPositionAlgorithm(100, 0.01, 0.2, 0.01)
        kpa.position_initialised = True
        actual_position = Vector([0.1, 0.2, 0.3])
        # Act
        position = kpa.step(PositionInput(position=Data(actual_position, 123.00)))
        # Assert
        self.assertIsNone(position.attitude)
        self.assertVectorAlmostEqual(Vector([0.196, 0.392, 0.588]), position.velocity)
        self.assertVectorAlmostEqual(Vector([0.051, 0.102, 0.153]), position.position)

    def test_can_update_kalman_with_velocity_only(self):
        # Arrange
        kpa = KalmanPositionAlgorithm(100, 0.1, 0.001, 0.01)
        kpa.velocity_initialised = True
        velocity = Vector([0.1, 0.2, 0.3])
        # Act
        position = kpa.step(PositionInput(velocity=Data(velocity, 123.00)))
        # Assert
        self.assertIsNone(position.attitude)
        self.assertVectorAlmostEqual(Vector([0.05, 0.10, 0.15]), position.acceleration)
        self.assertVectorAlmostEqual(Vector([0.05, 0.10, 0.15]), position.velocity)
        self.assertVectorAlmostEqual(Vector([0.0005, 0.001, 0.0015]), position.position)

    def test_can_update_kalman_with_acceleration_only(self):
        # Arrange
        kpa = KalmanPositionAlgorithm(100, 0.1, 0.2, 0.01)
        kpa.acceleration_initialised = True
        ao = AttitudeOutput(Vector([1, 2, 3]), Quaternion.identity(), Flags())
        # Act. Need 2 steps to get moving
        position = kpa.step(PositionInput(Data(ao, 123.00)))
        position = kpa.step(PositionInput(Data(ao, 123.01)))
        # Assert
        self.assertEqual(ao.attitude, position.attitude)
        self.assertVectorAlmostEqual(Vector([1, 2, 3]), position.acceleration)
        self.assertVectorAlmostEqual(Vector([0.01, 0.02, 0.03]), position.velocity)
        self.assertVectorAlmostEqual(Vector([0.00005, 0.0001, 0.00015]), position.position)

    def test_can_update_kalman_with_all_measurements(self):
        kpa = KalmanPositionAlgorithm(100, 0.01, 0.2, 0.1)
        kpa.position_initialised = True
        kpa.velocity_initialised = True
        kpa.acceleration_initialised = True
        actual_position = Vector([0.00005, 0.0001, 0.00015])
        velocity = Vector([0.01, 0.02, 0.03])
        ao = AttitudeOutput(Vector([1, 2, 3]), Quaternion.identity(), Flags())
        # Act
        position = kpa.step(PositionInput(attitude=Data(ao, 123.00), velocity=Data(velocity, 123.00), position=Data(actual_position, 123.0)))
        # Assert
        self.assertEqual(ao.attitude, position.attitude)
        self.assertVectorAlmostEqual(Vector([0.99, 1.98, 2.97]), position.acceleration)
        self.assertVectorAlmostEqual(Vector([0.005, 0.010, 0.015]), position.velocity)
        self.assertVectorAlmostEqual(Vector([0.00005, 0.0001, 0.00015]), position.position)

    def assertVectorAlmostEqual(self, expected: Vector, actual: Vector):
        tolerance = 0.01
        self.assertTrue(math.isclose(expected.x, actual.x, rel_tol=tolerance))
        self.assertTrue(math.isclose(expected.y, actual.y, rel_tol=tolerance))
        self.assertTrue(math.isclose(expected.z, actual.z, rel_tol=tolerance))
