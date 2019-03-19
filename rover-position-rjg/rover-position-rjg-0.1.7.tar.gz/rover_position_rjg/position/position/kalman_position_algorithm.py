import numpy as np

from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.kalman.kalman_filter import KalmanFilter
from rover_position_rjg.position.position.position import Position
from rover_position_rjg.position.position.position_algorithm import PositionAlgorithm, ABC
from rover_position_rjg.position.position.position_input import PositionInput


class KalmanPositionAlgorithmConfig:
    def __init__(self,
                 expected_frequency: float,
                 mean_position_error: float,
                 mean_velocity_error: float,
                 mean_acceleration_error: float):
        self.mean_acceleration_error = mean_acceleration_error
        self.mean_velocity_error = mean_velocity_error
        self.mean_position_error = mean_position_error
        self.expected_frequency = expected_frequency


# noinspection PyPep8Naming
class KalmanPositionAlgorithm(PositionAlgorithm, ABC):
    """Uses a Kalman filter to determine the rover's position
    and velocity."""
    kalman = ...  # type: KalmanFilter

    def __init__(self,
                 expected_frequency: float,
                 mean_position_error: float,
                 mean_velocity_error: float,
                 mean_acceleration_error: float):
        """
        Constructor. The mean errors help the filter to provide an accurate position
        as soon as it starts. They are replaced by measured values once the filter
        has been running for a while.
        :param expected_frequency: Expected frequency of samples. Used when updating
        the Kalman filter for the first time
        :param mean_position_error: RMS error of position measurement in metres
        :param mean_velocity_error: RMS error of the velocity measurement in m/s
        :param mean_acceleration_error: RMS error of the acceleration measurement in m/s/s
        """
        super().__init__()
        # x0: Initial state
        x0 = self.build_state(Vector.zero(), Vector.zero(), Vector.zero())
        # p0: Initial state covariance. Starts with initial measurement variances
        p0 = self.init_p0(mean_position_error, mean_velocity_error, mean_acceleration_error)
        # A: Transition matrix that calculates new state from rover_position_rjg.old state using equations of motion
        A = self.init_A(expected_frequency)
        # B: Control matrix. Set to None as we're not providing control inputs
        B = None
        # H: Observation matrix: contains ones for each measurement in the step
        H = self.init_H()
        # R: Observation co-variance. Reports cross talk between variables
        # Happens to be identical to p0 in the 3D case
        R = self.init_p0(mean_position_error, mean_velocity_error, mean_acceleration_error)
        # Q: Transition covariance matrix. Adds cross talk between inputs.
        Q = self.init_Q()
        self.kalman = KalmanFilter(x0, p0, A, B, H, R, Q)
        self.previous_timestamp = 0
        self.position_initialised = False
        self.velocity_initialised = False
        self.acceleration_initialised = False

    def step(self, data: PositionInput) -> Position:
        # Assume all inputs have the same timestamp
        timestamp = 0   # This will be overwritten as PositionInput must have at least one datum
        position = velocity = acceleration = Vector.zero()
        has_position = 0
        if data.position:
            has_position = 1
            timestamp = data.position.timestamp
            position = data.position.value
            self._initialise_position(position)
        has_velocity = 0
        if data.velocity:
            has_velocity = 1
            timestamp = data.velocity.timestamp
            velocity = data.velocity.value
            self._initialise_velocity(velocity)
        has_acceleration = 0
        attitude = None
        if data.attitude:
            has_acceleration = 1
            timestamp = data.attitude.timestamp
            acceleration = data.attitude.value.acceleration
            attitude = data.attitude.value.attitude
        self.update_observation_matrix(has_position, has_velocity, has_acceleration)
        self.update_transition_matrix(timestamp)
        z = self.build_state(position, velocity, acceleration)
        new_position = self.kalman.step(z)
        return self.to_position(new_position, attitude)

    def _initialise_position(self, position: Vector):
        """Sets the position in the Kalman filter directly to
        a new value. This is used to initialise the position
        without having to wait for the filter to converge."""
        if not self.position_initialised:
            self.kalman.x[0] = position.x
            self.kalman.x[3] = position.y
            self.kalman.x[6] = position.z
            self.position_initialised = True

    def _initialise_velocity(self, velocity: Vector):
        """Sets the velocity in the Kalman filter directly to
        a new value. This is used to initialise the velocity
        without having to wait for the filter to converge."""
        if not self.velocity_initialised:
            self.kalman.x[1] = velocity.x
            self.kalman.x[4] = velocity.y
            self.kalman.x[7] = velocity.z
            self.velocity_initialised = True

    def update_transition_matrix(self, timestamp):
        if self.previous_timestamp:
            # Calculate the time interval since the last update
            dt = timestamp - self.previous_timestamp
            at = 0.5*(dt**2)
            a = self.kalman.A
            a[0, 1] = a[1, 2] = a[3, 4] = a[4, 5] = a[6, 7] = a[7, 8] = dt
            a[0, 2] = a[3, 5] = a[6, 8] = at
        # else: This is the first iteration. Use the expected frequency
        # which is already encoded in the matrix.
        self.previous_timestamp = timestamp

    def update_observation_matrix(self, has_position: int, has_velocity: int, has_acceleration: int):
        """Changes the transition matrix to 'switch on' whichever measurements
        were actually provided by the PositionInput"""
        h = self.kalman.H
        h[0, 0] = h[3, 3] = h[6, 6] = has_position
        h[1, 1] = h[4, 4] = h[7, 7] = has_velocity
        h[2, 2] = h[5, 5] = h[8, 8] = has_acceleration

    @staticmethod
    def to_position(new_position: np.ndarray, attitude: Quaternion):
        acceleration = Vector([new_position.item(2), new_position.item(5), new_position.item(8)])
        velocity = Vector([new_position.item(1), new_position.item(4), new_position.item(7)])
        position = Vector([new_position.item(0), new_position.item(3), new_position.item(6)])
        return Position(attitude, acceleration, velocity, position)

    @staticmethod
    def build_state(position: Vector, velocity: Vector, acceleration: Vector):
        return np.array([
            [position.x],
            [velocity.x],
            [acceleration.x],
            [position.y],
            [velocity.y],
            [acceleration.y],
            [position.z],
            [velocity.z],
            [acceleration.z]
        ], dtype=float)

    @staticmethod
    def init_p0(mean_position_error: float, mean_velocity_error: float, mean_acceleration_error: float):
        """
        Generates the initial state covariance matrix. The initial values will be
        replaced by measured values as the filter runs but the filter will stabilise
        faster if these are estimated correctly.
        :param mean_position_error: RMS error of position measurement in metres
        :param mean_velocity_error: RMS error of the velocity measurement in m/s
        :param mean_acceleration_error: RMS error of the acceleration measurement in m/s/s
        :return:
        """
        d = mean_position_error**2
        v = mean_velocity_error**2
        a = mean_acceleration_error**2
        return np.array([
            [d, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, v, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, a, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, d, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, v, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, a, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, d, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, v, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, a],
        ], dtype=float)

    @staticmethod
    def init_A(expected_frequency: float):
        # dt and at will be overridden by _update_transition_matrix
        # when we know the real interval between samples
        dt = 1/expected_frequency
        at = 0.5*(dt**2)
        return np.array([
            [1, dt, at,  0,  0,  0,  0,  0,  0],
            [0,  1, dt,  0,  0,  0,  0,  0,  0],
            [0,  0,  1,  0,  0,  0,  0,  0,  0],
            [0,  0,  0,  1, dt, at,  0,  0,  0],
            [0,  0,  0,  0,  1, dt,  0,  0,  0],
            [0,  0,  0,  0,  0,  1,  0,  0,  0],
            [0,  0,  0,  0,  0,  0,  1, dt, at],
            [0,  0,  0,  0,  0,  0,  0,  1, dt],
            [0,  0,  0,  0,  0,  0,  0,  0,  1],
        ], dtype=float)

    @staticmethod
    def init_H():
        return np.identity(9)

    @staticmethod
    def init_Q():
        return np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
        ], dtype=float)
