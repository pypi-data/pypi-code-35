import math
from typing import List, Tuple

from rover_position_rjg.data.vector import Vector
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class ImuCalibrator:
    def __init__(self, offsets: NineDoFData, multipliers: NineDoFData):
        self.offsets = offsets
        self.multipliers = multipliers

    def set_x_y_acceleration_biases(self, measurements: List[Tuple[Vector, Vector]]):
        """
        Calculates the accelerometer x and y biases from pairs of measurements
        taken 180 degrees apart on a plane surface. The rotation must be around
        the z axis It doesn't matter what angle the plane is at relative to
        the horizontal. The biases are the averages of the midpoints of each pair of
        measurements.
        :param measurements: pairs of measurements made 180 degrees apart
        """
        midpoints = self._get_average(measurements)
        self.offsets.acceleration.value = Vector([midpoints.x, midpoints.y, self.offsets.acceleration.value.z])

    def set_acceleration_biases_to_1_g(self, measurement: Vector):
        """Adjusts the bias of the vertical axis (z) to give a magnitude
        of exactly 1 g. This avoids a small but annoying net acceleration
        after removing g from the overall acceleration. Assumes the scaling
        is correct and the biases for x and y have been set."""
        offset = self.offsets.acceleration.value
        multiplier = self.multipliers.acceleration.value
        scaled = (measurement - offset).scale(multiplier)
        m = scaled.magnitude()
        z = scaled.z
        scaled_delta_z = z - math.sqrt(z**2 + 1 - m**2)    # Positive root of quadratic equation for scaled_delta_z
        new_offset_z = offset.z + scaled_delta_z / multiplier.z
        new_offset = Vector([offset.x, offset.y, new_offset_z])
        self.offsets.acceleration.value = new_offset

    def set_x_y_magnetic_field_biases(self, measurements: List[Tuple[Vector, Vector]]):
        """
        Calculates the magnetometer x and y biases from pairs of measurements
        taken 180 degrees apart on a plane surface. The rotation must be around
        the z axis It doesn't matter what angle the plane is at relative to
        the horizontal. The biases are the averages of the midpoints of each pair of
        measurements.
        :param measurements: pairs of measurements made 180 degrees apart
        """
        midpoints = self._get_average(measurements)
        self.offsets.magnetic_field.value = Vector([midpoints.x, midpoints.y, self.offsets.magnetic_field.value.z])

    @staticmethod
    def _get_average(measurements: List[Tuple[Vector, Vector]]):
        total = Vector.zero()
        for measurement in measurements:
            total += (measurement[0] + measurement[1])
        return total / (2 * len(measurements))
