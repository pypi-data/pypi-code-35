import math
from typing import Tuple

import numpy as np

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.flags import Flags
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.calibration.simple_scaler import SimpleScaler
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class ImuScaler(SimpleScaler[NineDoFData]):
    INSIDE_ZERO_LIMITS_STATUS_BIT = 0
    CALIBRATING_STATUS_BIT = 2
    G = 1

    sensitivity_to_x = Vector([     0,  0.012,    0.000])
    sensitivity_to_y = Vector([-0.008,      0,   -0.015])
    sensitivity_to_z = Vector([-0.01,   0.008,        0])

    """Provides signal conditioning as well as scaling for an IMU"""
    def __init__(self,
                 offset: NineDoFData = NineDoFData.zero(),
                 multiplier: NineDoFData = NineDoFData.one(),
                 gyro_zero_band_height: Vector = Vector([9.5, 7.0, 5.0]),
                 gyro_zero_band_num_samples: int = 46,
                 cross_axis_sensitivities: Tuple[Vector, Vector, Vector] = (sensitivity_to_x, sensitivity_to_y, sensitivity_to_z)
                 ):
        super().__init__(offset, multiplier)
        self.gyro_zero_band_num_samples = gyro_zero_band_num_samples
        self.gyro_zero_band_height = gyro_zero_band_height
        self.gyro_zero_upper_limit: Vector = None
        self.gyro_zero_lower_limit: Vector = None
        self._set_gyro_zero_limits()
        self.cross_axis_sensitivities = cross_axis_sensitivities
        self._calibration_gyro_samples = []
        self._calibration_acc_samples = []
        self.calibrating = False

    def load(self, filename: str) -> None:
        super().load(filename)
        self._set_gyro_zero_limits()

    def calibrate(self) -> None:
        self._calibration_gyro_samples = []
        self._calibration_acc_samples = []
        self.calibrating = True

    def _add_calibration_sample(self, gyro: Vector, acc: Vector) -> None:
        self._calibration_gyro_samples.append(gyro.values)
        self._calibration_acc_samples.append(acc.values)
        if len(self._calibration_gyro_samples) >= self.gyro_zero_band_num_samples:
            self._calibrate_gyro_offset()
            self._calibration_gyro_samples.clear()
            self._calibrate_acceleration()
            self._calibration_acc_samples.clear()
            self.calibrating = False

    def _calibrate_gyro_offset(self):
        np_array = np.array(self._calibration_gyro_samples)
        self.gyro_zero_band_height = Vector(list(np.std(np_array, axis=0)))
        self.offset.angular_velocity.value = Vector(list(np.average(np_array, axis=0)))
        self._set_gyro_zero_limits()

    def _calibrate_acceleration(self):
        """Modifies the acceleration z-offset to give an acceleration magnitude of 1g
           Valid if the rover is within +- 5 degrees of horizontal."""
        np_array = np.array(self._calibration_acc_samples)
        raw_samples = Vector(list(np.average(np_array, axis=0)))
        scaled_samples = (raw_samples - self.offset.acceleration.value).scale(self.multiplier.acceleration.value)
        target_scaled_z = math.sqrt(math.fabs(self.G - scaled_samples.x**2 - scaled_samples.y**2))
        z_offset = raw_samples.z - (target_scaled_z / self.multiplier.acceleration.value.z)
        old = self.offset.acceleration.value
        self.offset.acceleration.value = Vector([old.x, old.y, z_offset])

    def scale(self, data: Data[NineDoFData]) -> Data[NineDoFData]:
        acc = data.value.acceleration.value
        gyro = data.value.angular_velocity.value
        mag = data.value.magnetic_field.value
        cross_axis_offset = self._get_cross_axis_offset(acc)
        if self.calibrating:
            self._add_calibration_sample(gyro, acc)
        else:
            in_zero_limits = self._adjust_gyro_offset(gyro, data.timestamp)
            data.value.status[self.INSIDE_ZERO_LIMITS_STATUS_BIT] = in_zero_limits
        data.value.status[self.CALIBRATING_STATUS_BIT] = self.calibrating

        new_acc = Vector([acc.x - cross_axis_offset.x, acc.y - cross_axis_offset.y, acc.z - cross_axis_offset.z])
        new_data = self._build_data(data, new_acc, gyro, mag, data.value.status)
        return super().scale(new_data)

    def _get_cross_axis_offset(self, acceleration: Vector) -> Vector:
        by_dx = self.cross_axis_sensitivities[0] * acceleration.x
        by_dy = self.cross_axis_sensitivities[1] * acceleration.y
        by_dz = self.cross_axis_sensitivities[2] * acceleration.z
        return by_dx + by_dy + by_dz

    def _adjust_gyro_offset(self, angular_velocity: Vector, timestamp: float) -> bool:
        if self.gyro_zero_upper_limit > angular_velocity and angular_velocity > self.gyro_zero_lower_limit:
            gyro_average = self.offset.angular_velocity.value
            gyro_average = ((gyro_average * (self.gyro_zero_band_num_samples - 1)) + angular_velocity) / self.gyro_zero_band_num_samples
            self.offset.angular_velocity.value = gyro_average
            self._set_gyro_zero_limits()
            # print('Set gyro bias to {} at {}'.format(self.offset.angular_velocity.value, timestamp))
            return True
        return False

    def _set_gyro_zero_limits(self):
        gyro_offset = self.offset.angular_velocity.value
        self.gyro_zero_upper_limit = gyro_offset + self.gyro_zero_band_height
        self.gyro_zero_lower_limit = gyro_offset - self.gyro_zero_band_height

    @staticmethod
    def _build_data(data: Data[NineDoFData], acceleration: Vector, angular_velocity: Vector, magnetic_field: Vector, status: Flags) -> Data[NineDoFData]:
        acc_data = Data(acceleration, data.value.acceleration.timestamp)
        gyro_data = Data(angular_velocity, data.value.angular_velocity.timestamp)
        mag_data = Data(magnetic_field, data.value.magnetic_field.timestamp)
        nine_dof = NineDoFData(acc_data, gyro_data, mag_data, data.value.temperature, status)
        return Data(nine_dof, data.timestamp)
