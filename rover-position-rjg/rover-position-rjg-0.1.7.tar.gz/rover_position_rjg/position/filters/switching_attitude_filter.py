from rover_position_rjg.data.data_filter import *
from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.attitude.attitude_algorithm import AttitudeAlgorithm
from rover_position_rjg.position.filters.attitude_filter import AttitudeOutput
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class SwitchingAttitudeFilterConfig:
    def __init__(self, acceleration_sensitivity: float = 0.005, cool_down: float = 0.2):
        self.acceleration_sensitivity = acceleration_sensitivity
        self.cool_down = cool_down


class SwitchingAttitudeFilter(DataFilter[NineDoFData, AttitudeOutput]):
    """Like AttitudeFilter except that it switches between 2 different
    attitude algorithms. The 'static' algorithm is assumed to be
    sensitive to acceleration and changing magnetic fields. e.g Madgwick
    The dynamic algorithm relies almost entirely on gyroscope data
    for the heading."""
    STATIONARY_STATUS_BIT = 1

    def __init__(self,
                 static_algorithm: AttitudeAlgorithm,
                 dynamic_algorithm: AttitudeAlgorithm,
                 acceleration_sensitivity: float = 0.005,
                 cool_down: float = 0.2,
                 name: str = ''):
        """
        :param static_algorithm: an algorithm that's more accurate when stationary
        :param dynamic_algorithm: an algorithm that's more accurate when moving
        :param acceleration_sensitivity: acceleration in g that triggers the switch
        from rover_position_rjg.the static to the dynamic algorithm.
        :param cool_down: time to wait in seconds before switching to the static
        algorithm once acceleration has ended
        :param name: the filter name
        """
        super().__init__(name)
        self.g = Vector([0, 0, 1])
        self.static_algorithm = static_algorithm
        self.dynamic_algorithm = dynamic_algorithm
        self.current_algorithm = self.static_algorithm
        self.acceleration_sensitivity = acceleration_sensitivity
        self.cool_down = cool_down
        self.previous_attitude = Quaternion.identity()
        self.previous_timestamp = 0
        self.previous_in_tolerance = False
        self.switch_to_static_time = 0
        self.start_timestamp = 0

    def reset(self):
        """Switches back to the static algorithm. Useful if the system has been
        restarted after having been paused for a while"""
        self.static_algorithm.reset()
        self.current_algorithm = self.static_algorithm

    def receive(self, data: Data[NineDoFData]) -> None:
        magnitude = data.value.acceleration.value.magnitude()
        in_tolerance = abs(magnitude - 1) < self.acceleration_sensitivity
        timestamp = data.value.angular_velocity.timestamp
        if not self.start_timestamp:
            self.start_timestamp = timestamp

        # Switch algorithm if necessary
        if self.current_algorithm is self.static_algorithm:
            if not in_tolerance:
                # print('Switching to Dynamic Attitude Algorithm at {:.4f}g, heading {}, time {}'.format(magnitude, self.previous_attitude.to_tait_bryan(), data.timestamp - self.start_timestamp))
                self.dynamic_algorithm.initialise(self.previous_attitude, self.previous_timestamp)
                self.current_algorithm = self.dynamic_algorithm
        else:
            if in_tolerance:
                if not self.previous_in_tolerance:
                    self.previous_in_tolerance = True
                    self.switch_to_static_time = timestamp + self.cool_down
                if timestamp >= self.switch_to_static_time:
                    # print('Switching to Static Attitude Algorithm after {:.1f}s, heading {}, time {}'.format(self.cool_down, self.previous_attitude.to_tait_bryan(), data.timestamp - self.start_timestamp))
                    self.static_algorithm.reset()
                    self.current_algorithm = self.static_algorithm
                    self.previous_in_tolerance = False
            else:
                self.previous_in_tolerance = False
        self.previous_timestamp = timestamp

        # Update the attitude and return
        self.previous_attitude = self.current_algorithm.step(data.value)
        acceleration = self.previous_attitude.rotate(data.value.acceleration.value) - self.g
        data.value.status[self.STATIONARY_STATUS_BIT] = self.current_algorithm == self.static_algorithm
        output = AttitudeOutput(acceleration, self.previous_attitude, data.value.status)
        self.send(Data(output, data.timestamp))
