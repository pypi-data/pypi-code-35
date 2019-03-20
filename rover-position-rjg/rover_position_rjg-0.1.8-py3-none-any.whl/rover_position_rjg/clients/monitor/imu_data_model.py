from rover_position_rjg.data.vector import Vector
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class ImuDataModel:
    actual = ...  # type: NineDoFData
    raw = ...  # type: NineDoFData

    def __init__(self):
        self.raw = NineDoFData.zero()
        self.actual = NineDoFData.zero()
        self.target_magnitudes = Vector([1, 0, 0.489925])

    def get_actual_error(self) -> Vector:
        mag_acc = self.actual.acceleration.value.magnitude()
        mag_av = self.actual.angular_velocity.value.magnitude()
        mag_mag = self.actual.magnetic_field.value.magnitude()
        magnitudes = Vector([mag_acc, mag_av, mag_mag])
        return magnitudes - self.target_magnitudes

    def get_relative_magnetic_field(self, field: float):
        earth_field = self.target_magnitudes.z
        return field / earth_field
