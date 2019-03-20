from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.position.attitude.attitude_algorithm import AttitudeAlgorithm
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class DummyAttitudeAlgorithm(AttitudeAlgorithm):
    def __init__(self):
        super().__init__()

    def reset(self):
        pass

    def initialise(self, attitude: Quaternion, timestamp: float):
        pass

    def step(self, data: NineDoFData) -> Quaternion:
        return Quaternion.identity()
