from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.attitude.attitude_algorithm import AttitudeAlgorithm
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class SimpleAttitudeAlgorithm(AttitudeAlgorithm):
    def __init__(self):
        super().__init__()
        self.attitude = Quaternion.identity()
        self.previous_timestamp = 0

    def reset(self):
        self.attitude = Vector.zero()
        self.previous_timestamp = 0
        self.initialised = False

    def initialise(self, attitude: Quaternion, timestamp: float):
        self.attitude = attitude
        self.previous_timestamp = timestamp
        self.initialised = True

    def step(self, data: NineDoFData) -> Quaternion:
        timestamp = data.angular_velocity.timestamp
        if self.initialised:
            # Integrate angles
            dt = timestamp - self.previous_timestamp
            self.previous_timestamp = timestamp
            delta_tait_bryan = data.angular_velocity.value * dt
            delta_q = Quaternion.from_tait_bryan_radians(delta_tait_bryan)
            q = self.attitude @ delta_q
            self.attitude = q.normalise()
        else:
            # Initialise quaternion from rover_position_rjg.magnetic field and gravity
            self.initialise(self.quaternion_from_imu(data), timestamp)
        return self.attitude
