import math

from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.position.attitude.attitude_algorithm import AttitudeAlgorithm
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


# noinspection PyPep8Naming,SpellCheckingInspection
class ModifiedMadgwick(AttitudeAlgorithm):
    # Below 2 it generates a significant drift up and down in velocity
    gyroMeasError = math.radians(2)  # gyroscope measurement error in rad/s (default 5 deg/s)
    beta = math.sqrt(3.0 / 4.0) * gyroMeasError  # compute beta
    nwu_to_enu = Quaternion(1/math.sqrt(2), 0, 0, 1/math.sqrt(2))

    """An implementation of Madgwick's algorithm for MARG that's a close
    as possible to the version in his paper."""

    def __init__(self):
        super().__init__()
        # print('Modified Madgwick beta={:5.3f}'.format(ModifiedMadgwick.beta))
        self.previous_timestamp = 0
        # estimated orientation quaternion elements with initial conditions
        self.q0, self.q1, self.q2, self.q3 = 1, 0, 0, 0

    def reset(self):
        self.__init__()

    def initialise(self, attitude: Quaternion, timestamp: float):
        # Rotate from rover_position_rjg.ENU to NWU or we'll start Madgwick out facing the wrong way
        q = (-self.nwu_to_enu) @ attitude
        self.q0, self.q1, self.q2, self.q3 = q.w, q.i, q.j, q.k
        self.previous_timestamp = timestamp
        self.initialised = True

    def step(self, data: NineDoFData) -> Quaternion:
        acc = data.acceleration.value
        gyro = data.angular_velocity.value
        mag = data.magnetic_field.value
        timestamp = data.angular_velocity.timestamp
        if self.initialised:
            deltat = timestamp - self.previous_timestamp
            self.previous_timestamp = timestamp
            self._filterUpdate(deltat, gyro.x, gyro.y, gyro.z, acc.x, acc.y, acc.z, mag.x, mag.y, mag.z)
            # Madgwick uses the axes NWU. We want ENU so rotate the output by 90 degrees
            # There may be a more efficient way to do this by messing with the inputs but
            # that seems to lead to cross talk between the different axes so I'll play
            # it safe and use a Quaternion rotation.
            madgwick_output = Quaternion(self.q0, self.q1, self.q2, self.q3)
            return self.nwu_to_enu @ madgwick_output
        else:
            # Initialise quaternion from rover_position_rjg.magnetic field and gravity
            from_imu = self.quaternion_from_imu(data)
            self.initialise(from_imu, timestamp)
            return from_imu

    # Note that Madgwick has his real world axes in the order North West Up.
    # We want to use East North Up so we need to rotate Madgwick's output by 90 degrees.
    def _filterUpdate(self, deltat: float, gx: float, gy: float, gz: float, ax: float, ay: float, az: float, mx: float, my: float, mz: float):
        norm = 0.0
        s0 = s1 = s2 = s3 = 0.0
        qDot1 = qDot2 = qDot3 = qDot4 = 0.0
        hx = hy = 0.0
        _2q0mx = _2q0my = _2q0mz = _2q1mx = 0.0
        _2bx = _2bz = _4bx = _4bz = 0.0
        _2q0 = _2q1 = _2q2 = _2q3 = _2q0q2 = _2q2q3 = 0.0
        q0q0 = q0q1 = q0q2 = q0q3 = 0.0
        q1q1 = q1q2 = q1q3 = q2q2 = q2q3 = q3q3 = 0.0

        # Rate of change of quaternion from rover_position_rjg.gyroscope
        qDot1 = 0.5 * (-self.q1 * gx - self.q2 * gy - self.q3 * gz)
        qDot2 = 0.5 * (self.q0 * gx + self.q2 * gz - self.q3 * gy)
        qDot3 = 0.5 * (self.q0 * gy - self.q1 * gz + self.q3 * gx)
        qDot4 = 0.5 * (self.q0 * gz + self.q1 * gy - self.q2 * gx)

        # normalise the accelerometer measurement
        norm = math.sqrt(ax * ax + ay * ay + az * az)
        if norm != 0:
            ax /= norm
            ay /= norm
            az /= norm

        # normalise the magnetometer measurement
        norm = math.sqrt(mx * mx + my * my + mz * mz)
        if norm != 0:
            mx /= norm
            my /= norm
            mz /= norm

        # Auxiliary variables to avoid repeated arithmetic
        _2q0mx = 2.0 * self.q0 * mx
        _2q0my = 2.0 * self.q0 * my
        _2q0mz = 2.0 * self.q0 * mz
        _2q1mx = 2.0 * self.q1 * mx
        _2q0 = 2.0 * self.q0
        _2q1 = 2.0 * self.q1
        _2q2 = 2.0 * self.q2
        _2q3 = 2.0 * self.q3
        _2q0q2 = 2.0 * self.q0 * self.q2
        _2q2q3 = 2.0 * self.q2 * self.q3
        q0q0 = self.q0 * self.q0
        q0q1 = self.q0 * self.q1
        q0q2 = self.q0 * self.q2
        q0q3 = self.q0 * self.q3
        q1q1 = self.q1 * self.q1
        q1q2 = self.q1 * self.q2
        q1q3 = self.q1 * self.q3
        q2q2 = self.q2 * self.q2
        q2q3 = self.q2 * self.q3
        q3q3 = self.q3 * self.q3

        # Reference direction of Earth's magnetic field
        hx = mx * q0q0 - _2q0my * self.q3 + _2q0mz * self.q2 + mx * q1q1 + _2q1 * my * self.q2 + _2q1 * mz * self.q3 - mx * q2q2 - mx * q3q3
        hy = _2q0mx * self.q3 + my * q0q0 - _2q0mz * self.q1 + _2q1mx * self.q2 - my * q1q1 + my * q2q2 + _2q2 * mz * self.q3 - my * q3q3
        _2bx = math.sqrt(hx * hx + hy * hy)
        _2bz = -_2q0mx * self.q2 + _2q0my * self.q1 + mz * q0q0 + _2q1mx * self.q3 - mz * q1q1 + _2q2 * my * self.q3 - mz * q2q2 + mz * q3q3
        _4bx = 2.0 * _2bx
        _4bz = 2.0 * _2bz
        _8bx = 2.0 * _4bx
        _8bz = 2.0 * _4bz

        # Gradient decent algorithm corrective step
        s0 = -_2q2 * (2.0 * (q1q3 - q0q2) - ax) + _2q1 * (2.0 * (q0q1 + q2q3) - ay) + -_4bz * self.q2 * (
                    _4bx * (0.5 - q2q2 - q3q3) + _4bz * (q1q3 - q0q2) - mx) + (-_4bx * self.q3 + _4bz * self.q1) * (
                         _4bx * (q1q2 - q0q3) + _4bz * (q0q1 + q2q3) - my) + _4bx * self.q2 * (
                         _4bx * (q0q2 + q1q3) + _4bz * (0.5 - q1q1 - q2q2) - mz)
        s1 = _2q3 * (2.0 * (q1q3 - q0q2) - ax) + _2q0 * (2.0 * (q0q1 + q2q3) - ay) + -4.0 * self.q1 * (
                    2.0 * (0.5 - q1q1 - q2q2) - az) + _4bz * self.q3 * (
                         _4bx * (0.5 - q2q2 - q3q3) + _4bz * (q1q3 - q0q2) - mx) + (_4bx * self.q2 + _4bz * self.q0) * (
                         _4bx * (q1q2 - q0q3) + _4bz * (q0q1 + q2q3) - my) + (_4bx * self.q3 - _8bz * self.q1) * (
                         _4bx * (q0q2 + q1q3) + _4bz * (0.5 - q1q1 - q2q2) - mz)
        s2 = -_2q0 * (2.0 * (q1q3 - q0q2) - ax) + _2q3 * (2.0 * (q0q1 + q2q3) - ay) + (-4.0 * self.q2) * (
                    2.0 * (0.5 - q1q1 - q2q2) - az) + (-_8bx * self.q2 - _4bz * self.q0) * (
                         _4bx * (0.5 - q2q2 - q3q3) + _4bz * (q1q3 - q0q2) - mx) + (_4bx * self.q1 + _4bz * self.q3) * (
                         _4bx * (q1q2 - q0q3) + _4bz * (q0q1 + q2q3) - my) + (_4bx * self.q0 - _8bz * self.q2) * (
                         _4bx * (q0q2 + q1q3) + _4bz * (0.5 - q1q1 - q2q2) - mz)
        s3 = _2q1 * (2.0 * (q1q3 - q0q2) - ax) + _2q2 * (2.0 * (q0q1 + q2q3) - ay) + (
                    -_8bx * self.q3 + _4bz * self.q1) * (_4bx * (0.5 - q2q2 - q3q3) + _4bz * (q1q3 - q0q2) - mx) + (
                         -_4bx * self.q0 + _4bz * self.q2) * (_4bx * (q1q2 - q0q3) + _4bz * (q0q1 + q2q3) - my) + (
                         _4bx * self.q1) * (_4bx * (q0q2 + q1q3) + _4bz * (0.5 - q1q1 - q2q2) - mz)

        norm = math.sqrt(s0 * s0 + s1 * s1 + s2 * s2 + s3 * s3)  # normalise step magnitude
        if norm != 0:
            s0 /= norm
            s1 /= norm
            s2 /= norm
            s3 /= norm

        # Apply feedback step
        qDot1 -= ModifiedMadgwick.beta * s0
        qDot2 -= ModifiedMadgwick.beta * s1
        qDot3 -= ModifiedMadgwick.beta * s2
        qDot4 -= ModifiedMadgwick.beta * s3

        # Integrate rate of change of quaternion to yield quaternion
        self.q0 += qDot1 * deltat
        self.q1 += qDot2 * deltat
        self.q2 += qDot3 * deltat
        self.q3 += qDot4 * deltat

        # Normalise quaternion
        norm = math.sqrt(self.q0 * self.q0 + self.q1 * self.q1 + self.q2 * self.q2 + self.q3 * self.q3)
        if norm != 0:
            self.q0 /= norm
            self.q1 /= norm
            self.q2 /= norm
            self.q3 /= norm
