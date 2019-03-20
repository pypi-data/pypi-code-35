from rover_position_rjg.data.data import Data
from rover_position_rjg.data.data_filter import DataFilter
from rover_position_rjg.data.flags import Flags
from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector

from rover_position_rjg.position.attitude.attitude_algorithm import AttitudeAlgorithm
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class AttitudeOutput:
    def __init__(self, acceleration: Vector, attitude: Quaternion, status: Flags):
        self.acceleration = acceleration
        self.attitude = attitude
        self.status = status


class AttitudeFilter(DataFilter[NineDoFData, AttitudeOutput]):
    """Uses some algorithm to determine the orientation of a 9 degree
    of freedom IMU. Also provides the acceleration in the
    real world frame of reference excluding g."""

    def __init__(self, algorithm: AttitudeAlgorithm, name: str = ''):
        super().__init__(name)
        self.algorithm = algorithm
        self.g = Vector([0, 0, 1])

    def receive(self, data: Data[NineDoFData]) -> None:
        attitude = self.algorithm.step(data.value)
        acceleration = attitude.rotate(data.value.acceleration.value) - self.g
        output = AttitudeOutput(acceleration, attitude, data.value.status)
        self.send(Data(output, data.value.acceleration.timestamp))
