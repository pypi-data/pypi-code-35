from typing import Tuple

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.calibration.simple_scaler import SimpleScaler
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class ImuScaler(SimpleScaler[NineDoFData]):
    sensitivity_to_minus_x = Vector([      0, -0.0135, -0.0155])
    sensitivity_to_minus_y = Vector([-0.0035,       0, -0.0094])
    sensitivity_to_minus_z = Vector([  0.082,   0.028,       0])
    sensitivity_to_plus_x =  Vector([      0,  0.0210,  0.0155])
    sensitivity_to_plus_y =  Vector([  0.030,       0,  0.020])
    sensitivity_to_plus_z =  Vector([  0.026,  0.0021,       0])
    scale_minus_x = 1/16000
    scale_plus_x = 1/16626
    scale_minus_y = 1/16423
    scale_plus_y  = 1/16196
    scale_minus_z = 1/16280
    scale_plus_z = 1/16425

    i_x = 0
    i_y = 1
    i_z = 2
    i_minus = 0
    i_plus = 1

    """Provides signal conditioning as well as scaling for an IMU"""
    def __init__(self,
                 offset: NineDoFData = NineDoFData.zero(),
                 multiplier: NineDoFData = NineDoFData.one(),
                 gyro_zero_band_height: Vector = Vector([6.5, 8, 5.5]),
                 gyro_zero_band_num_samples: int = 46,
                 cross_axis_sensitivities: (Tuple[Vector, Vector, Vector], Tuple[Vector, Vector, Vector])
                    = ((sensitivity_to_minus_x, sensitivity_to_minus_y, sensitivity_to_minus_z),
                       (sensitivity_to_plus_x, sensitivity_to_plus_y, sensitivity_to_plus_z))
                 ):
        super().__init__(offset, multiplier)
        self.gyro_zero_band_num_samples = gyro_zero_band_num_samples
        self.gyro_zero_band_height = gyro_zero_band_height
        self.gyro_zero_upper_limit: Vector = None
        self.gyro_zero_lower_limit: Vector = None
        self._set_gyro_zero_limits()
        self.cross_axis_sensitivities = cross_axis_sensitivities

    def load(self, filename: str) -> None:
        super().load(filename)
        self._set_gyro_zero_limits()

    def scale(self, data: Data[NineDoFData]) -> Data[NineDoFData]:
        acc = data.value.acceleration.value
        gyro = data.value.angular_velocity.value
        mag = data.value.magnetic_field.value
        new_gyro = self._scale_gyro(gyro)
        new_acc = self._scale_accelerations(acc)
        new_mag = self._scale_mag(mag)
        return self._build_data(data, new_acc, new_gyro, new_mag)

    def _scale_mag(self, raw: Vector) -> Vector:
        return (raw - self.offset.magnetic_field.value).scale(self.multiplier.magnetic_field.value)

    def _scale_gyro(self, raw: Vector) -> Vector:
        self._adjust_gyro_offset(raw)
        return (raw - self.offset.angular_velocity.value).scale(self.multiplier.angular_velocity.value)

    def _scale_accelerations(self, raw: Vector) -> Vector:
        by_dx = by_dy = by_dz = Vector.zero()
        scale_x = scale_y = scale_z = 0
        raw_x = raw.x
        if raw_x < 0:
            by_dx = self.cross_axis_sensitivities[self.i_minus][self.i_x] * raw_x
            scale_x = self.scale_minus_x
        if raw_x > 0:
            by_dx = self.cross_axis_sensitivities[self.i_plus][self.i_x] * raw_x
            scale_x = self.scale_plus_x
        raw_y = raw.y
        if raw_y < 0:
            by_dy = self.cross_axis_sensitivities[self.i_minus][self.i_y] * raw_y
            scale_y = self.scale_minus_y
        if raw_y > 0:
            by_dy = self.cross_axis_sensitivities[self.i_plus][self.i_y] * raw_y
            scale_y = self.scale_plus_y
        raw_z = raw.z
        if raw_z < 0:
            by_dz = self.cross_axis_sensitivities[self.i_minus][self.i_z] * raw_z
            scale_z = self.scale_minus_z
        if raw_z > 0:
            by_dz = self.cross_axis_sensitivities[self.i_plus][self.i_z] * raw_z
            scale_z = self.scale_plus_z
        cross_axis_offsets = by_dx + by_dy + by_dz
        x = (raw_x - cross_axis_offsets.x) * scale_x
        y = (raw_y - cross_axis_offsets.y) * scale_y
        z = (raw_z - cross_axis_offsets.z) * scale_z
        return Vector([x, y, z])

    def _adjust_gyro_offset(self, angular_velocity: Vector):
        if self.gyro_zero_upper_limit > angular_velocity and angular_velocity > self.gyro_zero_lower_limit:
            gyro_average = self.offset.angular_velocity.value
            gyro_average = ((gyro_average * (self.gyro_zero_band_num_samples - 1)) + angular_velocity) / self.gyro_zero_band_num_samples
            self.offset.angular_velocity.value = gyro_average
            self._set_gyro_zero_limits()
            # print('Set gyro bias to {}'.format(self.offset.angular_velocity.value))

    def _set_gyro_zero_limits(self):
        gyro_offset = self.offset.angular_velocity.value
        self.gyro_zero_upper_limit = gyro_offset + self.gyro_zero_band_height
        self.gyro_zero_lower_limit = gyro_offset - self.gyro_zero_band_height

    @staticmethod
    def _build_data(data: Data[NineDoFData], acceleration: Vector, angular_velocity: Vector, magnetic_field: Vector) -> Data[NineDoFData]:
        acc_data = Data(acceleration, data.value.acceleration.timestamp)
        gyro_data = Data(angular_velocity, data.value.angular_velocity.timestamp)
        mag_data = Data(magnetic_field, data.value.magnetic_field.timestamp)
        nine_dof = NineDoFData(acc_data, gyro_data, mag_data, data.value.temperature)
        return Data(nine_dof, data.timestamp)
