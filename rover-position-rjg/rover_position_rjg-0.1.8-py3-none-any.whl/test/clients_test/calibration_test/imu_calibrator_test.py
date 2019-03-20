import unittest

from rover_position_rjg.clients.calibration.imu.imu_calibrator import ImuCalibrator
from rover_position_rjg.data.data import Data
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class ImuCalibratorTest(unittest.TestCase):
    def setUp(self):
        self.calibrator = ImuCalibrator(NineDoFData.zero(), NineDoFData.zero())

    def test_get_offsets(self):
        offsets = NineDoFData(Data(Vector([1.1, 1.2, 1.3]), 1), Data(Vector([2.1, 2.2, 2.3]), 1), Data(Vector([3.1, 3.2, 3.3]), 1), Data(4, 1))
        calibrator = ImuCalibrator(offsets, NineDoFData.zero())
        self.assertEqual(offsets, calibrator.offsets)

    def test_get_multipliers(self):
        multipliers = NineDoFData(Data(Vector([1.1, 1.2, 1.3]), 1), Data(Vector([2.1, 2.2, 2.3]), 1), Data(Vector([3.1, 3.2, 3.3]), 1), Data(4, 1))
        calibrator = ImuCalibrator(NineDoFData.zero(), multipliers)
        self.assertEqual(multipliers, calibrator.multipliers)

    def test_set_accelerometer_biases_from_single_measurement_pair(self):
        self.calibrator.offsets.acceleration.value = Vector([0, 0, 123])
        biases = Vector([100, 110, 120])
        error = Vector([50, 40, 30])
        measurements = [(biases-error, biases+error)]
        # Act
        self.calibrator.set_x_y_acceleration_biases(measurements)
        # Assert
        self.assertEqual(Vector([100, 110, 123]), self.calibrator.offsets.acceleration.value)

    def test_set_accelerometer_biases_from_multiple_measurement_pairs(self):
        self.calibrator.offsets.acceleration.value = Vector([0, 0, -123])
        centre1 = Vector([100, 110, 120])
        error1 = Vector([50, 40, 30])
        centre2 = Vector([106, 104, 122])
        error2 = Vector([12, 13, 14])
        measurements = [(centre1-error1, centre1+error1), (centre2-error2, centre2+error2)]
        # Act
        self.calibrator.set_x_y_acceleration_biases(measurements)
        # Assert
        self.assertEqual(Vector([103, 107, -123]), self.calibrator.offsets.acceleration.value)

    def test_set_acceleration_biases_to_1_g(self):
        multiplier = Vector([0.001, 0.002, 0.01])
        self.calibrator.multipliers.acceleration.value = multiplier
        offset = Vector([7, 3, 1.5])
        self.calibrator.offsets.acceleration.value = offset
        # Act
        measurement = Vector([50, 30, 110])
        self.calibrator.set_acceleration_biases_to_1_g(measurement)
        # Assert
        scaled = (measurement - offset).scale(multiplier)
        # print(scaled, scaled.magnitude())
        # print(self.calibrator.offsets.acceleration.value)
        after_scaled = (measurement - self.calibrator.offsets.acceleration.value).scale(multiplier)
        # print(after_scaled, after_scaled.magnitude())
        self.assertEqual(1.0, after_scaled.magnitude())

    def test_set_magnetometer_biases_from_single_measurement_pair(self):
        self.calibrator.offsets.magnetic_field.value = Vector([0, 0, 123])
        biases = Vector([100, 110, 120])
        error = Vector([50, 40, 30])
        measurements = [(biases-error, biases+error)]
        # Act
        self.calibrator.set_x_y_magnetic_field_biases(measurements)
        # Assert
        self.assertEqual(Vector([100, 110, 123]), self.calibrator.offsets.magnetic_field.value)

    def test_set_magnetometer_biases_from_multiple_measurement_pairs(self):
        self.calibrator.offsets.magnetic_field.value = Vector([0, 0, -123])
        centre1 = Vector([100, 110, 120])
        error1 = Vector([50, 40, 30])
        centre2 = Vector([106, 104, 122])
        error2 = Vector([12, 13, 14])
        measurements = [(centre1-error1, centre1+error1), (centre2-error2, centre2+error2)]
        # Act
        self.calibrator.set_x_y_magnetic_field_biases(measurements)
        # Assert
        self.assertEqual(Vector([103, 107, -123]), self.calibrator.offsets.magnetic_field.value)

