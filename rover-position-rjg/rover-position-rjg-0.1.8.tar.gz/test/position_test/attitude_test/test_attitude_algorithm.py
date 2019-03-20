import unittest

from rover_position_rjg.data.data import Data
from rover_position_rjg.position.attitude.attitude_algorithm import *


class TestAlgorithm(AttitudeAlgorithm):
    def reset(self):
        pass

    def initialise(self, attitude: Quaternion, timestamp: float):
        self.initialised = True

    def step(self, data: NineDoFData) -> Quaternion:
        pass


class AttitudeAlgorithmTest(unittest.TestCase):
    h = 1 / math.sqrt(2)
    zero = 4.654513802265776e-17
    g = Vector([0, 0, 1])
    m = Vector([0.00, 0.22, -0.43])

    def test_not_initialised_by_default(self):
        a = TestAlgorithm()
        self.assertFalse(a.initialised)

    def test_quaternion_from_imu_forwards(self):
        acc = self.g
        mag = self.m
        q = self.quaternion_from_imu(acc, mag)
        self.assertEqual(Quaternion(1.0, 0.0, 0.0, 0.0), q)

    def test_quaternion_from_imu_yaw_90(self):
        acc = Vector([0, 0, 1])
        mag = Vector([-0.22, 0.0, -0.43])
        q = self.quaternion_from_imu(acc, mag)
        self.assertEqual(Quaternion(self.h, 0.0, 0.0, -self.h), q)

    def test_quaternion_from_imu_roll_90(self):
        acc = Vector([0, 1, 0])
        mag = Vector([0, -0.43, -0.20])
        q = self.quaternion_from_imu(acc, mag)
        self.assertEqual(Quaternion(self.h, self.h, 0, 0), q)

    def test_quaternion_from_imu_pitch_90(self):
        acc = Vector([-1, 0, 0])
        mag = Vector([0.43, 0.20, 0])
        q = self.quaternion_from_imu(acc, mag)
        self.assertEqual(Quaternion(self.h, -self.zero, self.h, self.zero), q)

    def test_quaternion_from_imu_pitch_and_yaw(self):
        expected = Quaternion.from_tait_bryan(Vector([0, 30, 60]))
        acc = (-expected).rotate(self.g)
        mag = (-expected).rotate(self.m)
        actual = self.quaternion_from_imu(acc, mag)
        self.assertEqual(expected, actual)

    def test_quaternion_from_imu_roll_pitch_and_yaw(self):
        expected = Quaternion.from_tait_bryan(Vector([75, 30, 60]))
        acc = (-expected).rotate(self.g)
        mag = (-expected).rotate(self.m)
        print('a {} m {}'.format(acc, mag))
        actual = self.quaternion_from_imu(acc, mag)
        self.assertEqual(expected, actual)

    @staticmethod
    def quaternion_from_imu(acc: Vector, mag: Vector) -> Quaternion:
        data = NineDoFData(Data(acc, 123), Data(Vector.zero(), 124), Data(mag, 125), Data(22, 126))
        return AttitudeAlgorithm.quaternion_from_imu(data)
