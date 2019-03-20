import math
from abc import ABC, abstractmethod

from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class AttitudeAlgorithm(ABC):
    """A step wise algorithm for determining a device's attitude
    from gyroscope, accelerometer and magnetometer readings"""

    def __init__(self):
        self.initialised = False

    @abstractmethod
    def step(self, data: NineDoFData) -> Quaternion:
        """
        Updates the attitude estimate with the supplied IMU data
        :param data: the data
        :returns the new attitude
        """
        pass

    @abstractmethod
    def reset(self):
        """Resets the algorithm to its initial state. i.e. it behaves as
        if it had just been created."""
        pass

    @abstractmethod
    def initialise(self, attitude: Quaternion, timestamp: float):
        """
        Sets the current attitude estimate to the supplied value
        :param attitude: the desired attitude estimate
        :param timestamp: the time at which this attitude was calculated
        """
        pass

    @staticmethod
    def quaternion_from_imu(data: NineDoFData) -> Quaternion:
        """Creates a quaternion from the magnetic field and acceleration
        vectors in the data"""
        # Get roll and pitch directly from acceleration
        acc = data.acceleration.value
        roll = math.atan2(acc.y, acc.z)

        pitch = -math.atan2(acc.x, math.sqrt(acc.y**2 + acc.z**2))
        # Yaw is much harder!
        mag = data.magnetic_field.value
        sin_roll = math.sin(roll)
        cos_roll = math.cos(roll)
        vy = mag.z * sin_roll - mag.y * cos_roll
        vz = mag.y * sin_roll + mag.z * cos_roll
        vx = mag.x * math.cos(pitch) + vz * math.sin(pitch)
        yaw = math.atan2(vx, -vy)
        euler_angles = Vector([math.degrees(roll), math.degrees(pitch), math.degrees(yaw)])
        # print('Initial Tait Bryan angles: {}'.format(euler_angles))
        q = Quaternion.from_tait_bryan(euler_angles)
        # print('Initial Quaternion {}'.format(q))
        return q
