import math
import unittest
from rover_position_rjg.clients.monitor.imu_data_model import ImuDataModel
from rover_position_rjg.data.data import Data
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class ModelTest(unittest.TestCase):

    def test_initialises_properties(self):
        model = ImuDataModel()
        self.assertIsZero9DofData(model.raw)
        self.assertIsZero9DofData(model.actual)

    def test_get_initial_actual_error(self):
        model = ImuDataModel()
        error = model.get_actual_error()
        self.assertEqual(Vector([-1, 0, -0.489925]), error)

    def test_error_depends_on_actual(self):
        model = ImuDataModel()
        sqrt_half = math.sqrt(0.5)
        acc = Vector([sqrt_half, sqrt_half, sqrt_half])
        av = Vector([10, 20, 30])
        mag = Vector([1000, 500, 700])
        model.actual = NineDoFData(Data(acc, 10), Data(av, 10), Data(mag, 10), Data(10, 10))
        error = model.get_actual_error()
        self.assertEqual(error.x, acc.magnitude() - 1)
        self.assertEqual(error.y, av.magnitude() - 0)
        self.assertEqual(error.z, mag.magnitude() - 0.489925)

    def test_get_relative_magnetic_magnitude(self):
        model = ImuDataModel()
        self.assertAlmostEqual(1.000, model.get_relative_magnetic_field(0.489925), 5)
        self.assertAlmostEqual(1.051528, model.get_relative_magnetic_field(0.515170), 5)

    def assertIsZero9DofData(self, data: NineDoFData):
        self.assertIsZeroVector(data.acceleration.value)
        self.assertEqual(data.acceleration.timestamp, 0)
        self.assertIsZeroVector(data.angular_velocity.value)
        self.assertEqual(data.angular_velocity.timestamp, 0)
        self.assertIsZeroVector(data.magnetic_field.value)
        self.assertEqual(data.magnetic_field.timestamp, 0)
        self.assertEqual(data.temperature.value, 0)
        self.assertEqual(data.temperature.timestamp, 0)

    def assertIsZeroVector(self, vector: Vector):
        self.assertEqual(vector.x, 0)
        self.assertEqual(vector.y, 0)
        self.assertEqual(vector.z, 0)

if __name__ == '__main__':
    unittest.main()
