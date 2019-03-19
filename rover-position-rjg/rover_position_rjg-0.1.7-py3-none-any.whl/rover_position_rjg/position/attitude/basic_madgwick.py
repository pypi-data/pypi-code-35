import math

from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.position.attitude.attitude_algorithm import AttitudeAlgorithm
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


# noinspection PyPep8Naming,SpellCheckingInspection
class BasicMadgwick(AttitudeAlgorithm):
    gyroMeasError = 3.14159265358979 * (5 / 180.0)  # gyroscope measurement error in rad/s (default 5 deg/s)
    gyroMeasDrift = 3.14159265358979 * (0.2 / 180.0)  # gyroscope measurement error in rad/s/s (default 0.2f deg/s/s)
    # gyroMeasError = 3.14159265358979 * (2 / 180.0)  # gyroscope measurement error in rad/s (default 5 deg/s)
    # gyroMeasDrift = 3.14159265358979 * (0.05 / 180.0)  # gyroscope measurement error in rad/s/s (default 0.2f deg/s/s)
    beta = math.sqrt(3.0 / 4.0) * gyroMeasError  # compute beta
    zeta = math.sqrt(3.0 / 4.0) * gyroMeasDrift  # compute zeta
    nwu_to_enu = Quaternion(1/math.sqrt(2), 0, 0, 1/math.sqrt(2))

    """An implementation of Madgwick's algorithm for MARG that's a close
    as possible to the version in his paper."""

    def __init__(self):
        super().__init__()
        print('Basic Madgwick beta={:5.3f}, zeta={:5.3f}'.format(BasicMadgwick.beta, BasicMadgwick.zeta))
        self.deltat = 0
        self.previous_timestamp = 0
        # estimated orientation quaternion elements with initial conditions
        self.SEq_1, self.SEq_2, self.SEq_3, self.SEq_4 = 1, 0, 0, 0
        # reference direction of flux in earth frame
        self.b_x, self.b_z = 1, 0
        # estimate gyroscope biases error
        self.w_bx, self.w_by, self.w_bz = 0, 0, 0

    def reset(self):
        self.__init__()

    def initialise(self, attitude: Quaternion, timestamp: float):
        # Rotate from rover_position_rjg.ENU to NWU or we'll start Madgwick out facing the wrong way
        q = (-self.nwu_to_enu) @ attitude
        self.SEq_1, self.SEq_2, self.SEq_3, self.SEq_4 = q.w, q.i, q.j, q.k
        self.previous_timestamp = timestamp
        self.initialised = True

    def step(self, data: NineDoFData) -> Quaternion:
        acc = data.acceleration.value
        gyro = data.angular_velocity.value
        mag = data.magnetic_field.value
        timestamp = data.angular_velocity.timestamp
        if self.previous_timestamp > 0:
            self.deltat = timestamp - self.previous_timestamp
            self.previous_timestamp = timestamp
            self._filterUpdate(gyro.x, gyro.y, gyro.z, acc.x, acc.y, acc.z, mag.x, mag.y, mag.z)
            # Madgwick uses the axes NWU. We want ENU so rotate the output by 90 degrees
            # There may be a more efficient way to do this by messing with the inputs but
            # that seems to lead to cross talk between the different axes so I'll play
            # it safe and use a Quaternion rotation.
            madgwick_output = Quaternion(self.SEq_1, self.SEq_2, self.SEq_3, self.SEq_4)
            return self.nwu_to_enu @ madgwick_output
        else:
            # Initialise quaternion from rover_position_rjg.magnetic field and gravity
            from_imu = self.quaternion_from_imu(data)
            self.initialise(from_imu, timestamp)
            return from_imu

    # Note that Madgwick has his real world axes in the order North West Up.
    # We want to use East North Up so we need to rotate Madgwick's output by 90 degrees.
    def _filterUpdate(self, w_x: float, w_y: float, w_z: float, a_x: float, a_y: float, a_z: float, m_x: float, m_y: float, m_z: float):
        # local system variables
        norm = 0  # vector norm
        SEqDot_omega_1, SEqDot_omega_2, SEqDot_omega_3, SEqDot_omega_4 = 0, 0, 0, 0  # quaternion rate from rover_position_rjg.gyroscopes elements
        f_1, f_2, f_3, f_4, f_5, f_6 = 0, 0, 0, 0, 0, 0  # objective function elements
        J_11or24, J_12or23, J_13or22, J_14or21, J_32, J_33 = 0, 0, 0, 0, 0, 0  # objective function Jacobian elements
        J_41, J_42, J_43, J_44, J_51, J_52, J_53, J_54, J_61, J_62, J_63, J_64 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0
        SEqHatDot_1, SEqHatDot_2, SEqHatDot_3, SEqHatDot_4 = 0, 0, 0, 0  # estimated direction of the gyroscope error
        w_err_x, w_err_y, w_err_z = 0, 0, 0  # estimated direction of the gyroscope error (angular)
        h_x, h_y, h_z = 0, 0, 0  # computed flux in the earth frame

        # axulirary variables to avoid reapeated calcualtions
        halfSEq_1 = 0.5 * self.SEq_1
        halfSEq_2 = 0.5 * self.SEq_2
        halfSEq_3 = 0.5 * self.SEq_3
        halfSEq_4 = 0.5 * self.SEq_4
        twoSEq_1 = 2.0 * self.SEq_1
        twoSEq_2 = 2.0 * self.SEq_2
        twoSEq_3 = 2.0 * self.SEq_3
        twoSEq_4 = 2.0 * self.SEq_4
        twob_x = 2.0 * self.b_x
        twob_z = 2.0 * self.b_z
        twob_xSEq_1 = 2.0 * self.b_x * self.SEq_1
        twob_xSEq_2 = 2.0 * self.b_x * self.SEq_2
        twob_xSEq_3 = 2.0 * self.b_x * self.SEq_3
        twob_xSEq_4 = 2.0 * self.b_x * self.SEq_4
        twob_zSEq_1 = 2.0 * self.b_z * self.SEq_1
        twob_zSEq_2 = 2.0 * self.b_z * self.SEq_2
        twob_zSEq_3 = 2.0 * self.b_z * self.SEq_3
        twob_zSEq_4 = 2.0 * self.b_z * self.SEq_4
        SEq_1SEq_2 = 0
        SEq_1SEq_3 = self.SEq_1 * self.SEq_3
        SEq_1SEq_4 = 0
        SEq_2SEq_3 = 0
        SEq_2SEq_4 = self.SEq_2 * self.SEq_4
        SEq_3SEq_4 = 0
        twom_x = 2.0 * m_x
        twom_y = 2.0 * m_y
        twom_z = 2.0 * m_z

        # normalise the accelerometer measurement
        norm = math.sqrt(a_x * a_x + a_y * a_y + a_z * a_z)
        if norm != 0:
            a_x /= norm
            a_y /= norm
            a_z /= norm

        # normalise the magnetometer measurement
        norm = math.sqrt(m_x * m_x + m_y * m_y + m_z * m_z)
        if norm != 0:
            m_x /= norm
            m_y /= norm
            m_z /= norm

        # compute the objective function and Jacobian
        f_1 = twoSEq_2 * self.SEq_4 - twoSEq_1 * self.SEq_3 - a_x
        f_2 = twoSEq_1 * self.SEq_2 + twoSEq_3 * self.SEq_4 - a_y
        f_3 = 1.0 - twoSEq_2 * self.SEq_2 - twoSEq_3 * self.SEq_3 - a_z
        f_4 = twob_x * (0.5 - self.SEq_3 * self.SEq_3 - self.SEq_4 * self.SEq_4) + twob_z * (SEq_2SEq_4 - SEq_1SEq_3) - m_x
        f_5 = twob_x * (self.SEq_2 * self.SEq_3 - self.SEq_1 * self.SEq_4) + twob_z * (self.SEq_1 * self.SEq_2 + self.SEq_3 * self.SEq_4) - m_y
        f_6 = twob_x * (SEq_1SEq_3 + SEq_2SEq_4) + twob_z * (0.5 - self.SEq_2 * self.SEq_2 - self.SEq_3 * self.SEq_3) - m_z
        J_11or24 = twoSEq_3  # J_11 negated in matrix multiplication
        J_12or23 = 2.0 * self.SEq_4
        J_13or22 = twoSEq_1  # J_12 negated in matrix multiplication
        J_14or21 = twoSEq_2
        J_32 = 2.0 * J_14or21  # negated in matrix multiplication
        J_33 = 2.0 * J_11or24  # negated in matrix multiplication
        J_41 = twob_zSEq_3  # negated in matrix multiplication
        J_42 = twob_zSEq_4
        J_43 = 2.0 * twob_xSEq_3 + twob_zSEq_1  # negated in matrix multiplication
        J_44 = 2.0 * twob_xSEq_4 - twob_zSEq_2  # negated in matrix multiplication
        J_51 = twob_xSEq_4 - twob_zSEq_2  # negated in matrix multiplication
        J_52 = twob_xSEq_3 + twob_zSEq_1
        J_53 = twob_xSEq_2 + twob_zSEq_4
        J_54 = twob_xSEq_1 - twob_zSEq_3  # negated in matrix multiplication
        J_61 = twob_xSEq_3
        J_62 = twob_xSEq_4 - 2.0 * twob_zSEq_2
        J_63 = twob_xSEq_1 - 2.0 * twob_zSEq_3
        J_64 = twob_xSEq_2   

        # compute the gradient (matrix multiplication)
        SEqHatDot_1 = J_14or21 * f_2 - J_11or24 * f_1 - J_41 * f_4 - J_51 * f_5 + J_61 * f_6
        SEqHatDot_2 = J_12or23 * f_1 + J_13or22 * f_2 - J_32 * f_3 + J_42 * f_4 + J_52 * f_5 + J_62 * f_6
        SEqHatDot_3 = J_12or23 * f_2 - J_33 * f_3 - J_13or22 * f_1 - J_43 * f_4 + J_53 * f_5 + J_63 * f_6
        SEqHatDot_4 = J_14or21 * f_1 + J_11or24 * f_2 - J_44 * f_4 - J_54 * f_5 + J_64 * f_6
    
        # normalise the gradient to estimate direction of the gyroscope error
        norm = math.sqrt(SEqHatDot_1 * SEqHatDot_1 + SEqHatDot_2 * SEqHatDot_2 + SEqHatDot_3 * SEqHatDot_3 + SEqHatDot_4 * SEqHatDot_4)
        if norm != 0:
            SEqHatDot_1 = SEqHatDot_1 / norm
            SEqHatDot_2 = SEqHatDot_2 / norm
            SEqHatDot_3 = SEqHatDot_3 / norm
            SEqHatDot_4 = SEqHatDot_4 / norm

        # compute angular estimated direction of the gyroscope error
        w_err_x = twoSEq_1 * SEqHatDot_2 - twoSEq_2 * SEqHatDot_1 - twoSEq_3 * SEqHatDot_4 + twoSEq_4 * SEqHatDot_3
        w_err_y = twoSEq_1 * SEqHatDot_3 + twoSEq_2 * SEqHatDot_4 - twoSEq_3 * SEqHatDot_1 - twoSEq_4 * SEqHatDot_2
        w_err_z = twoSEq_1 * SEqHatDot_4 - twoSEq_2 * SEqHatDot_3 + twoSEq_3 * SEqHatDot_2 - twoSEq_4 * SEqHatDot_1

        # compute and remove the gyroscope baises
        self.w_bx += w_err_x * self.deltat * BasicMadgwick.zeta
        self.w_by += w_err_y * self.deltat * BasicMadgwick.zeta
        self.w_bz += w_err_z * self.deltat * BasicMadgwick.zeta
        w_x -= self.w_bx
        w_y -= self.w_by
        w_z -= self.w_bz

        # compute the quaternion rate measured by gyroscopes
        SEqDot_omega_1 = -halfSEq_2 * w_x - halfSEq_3 * w_y - halfSEq_4 * w_z
        SEqDot_omega_2 = halfSEq_1 * w_x + halfSEq_3 * w_z - halfSEq_4 * w_y
        SEqDot_omega_3 = halfSEq_1 * w_y - halfSEq_2 * w_z + halfSEq_4 * w_x
        SEqDot_omega_4 = halfSEq_1 * w_z + halfSEq_2 * w_y - halfSEq_3 * w_x
    
        # compute then integrate the estimated quaternion rate
        self.SEq_1 += (SEqDot_omega_1 - (BasicMadgwick.beta * SEqHatDot_1)) * self.deltat
        self.SEq_2 += (SEqDot_omega_2 - (BasicMadgwick.beta * SEqHatDot_2)) * self.deltat
        self.SEq_3 += (SEqDot_omega_3 - (BasicMadgwick.beta * SEqHatDot_3)) * self.deltat
        self.SEq_4 += (SEqDot_omega_4 - (BasicMadgwick.beta * SEqHatDot_4)) * self.deltat

        # normalise quaternion
        norm = math.sqrt(self.SEq_1 * self.SEq_1 + self.SEq_2 * self.SEq_2 + self.SEq_3 * self.SEq_3 + self.SEq_4 * self.SEq_4)
        if norm != 0:
            self.SEq_1 /= norm
            self.SEq_2 /= norm
            self.SEq_3 /= norm
            self.SEq_4 /= norm
    
        # compute flux in the earth frame
        SEq_1SEq_2 = self.SEq_1 * self.SEq_2  # recompute axulirary variables
        SEq_1SEq_3 = self.SEq_1 * self.SEq_3
        SEq_1SEq_4 = self.SEq_1 * self.SEq_4
        SEq_3SEq_4 = self.SEq_3 * self.SEq_4
        SEq_2SEq_3 = self.SEq_2 * self.SEq_3
        SEq_2SEq_4 = self.SEq_2 * self.SEq_4
        h_x = twom_x * (0.5 - self.SEq_3 * self.SEq_3 - self.SEq_4 * self.SEq_4) + twom_y * (SEq_2SEq_3 - SEq_1SEq_4) + twom_z * (SEq_2SEq_4 + SEq_1SEq_3)
        h_y = twom_x * (SEq_2SEq_3 + SEq_1SEq_4) + twom_y * (0.5 - self.SEq_2 * self.SEq_2 - self.SEq_4 * self.SEq_4) + twom_z * (SEq_3SEq_4 - SEq_1SEq_2)
        h_z = twom_x * (SEq_2SEq_4 - SEq_1SEq_3) + twom_y * (SEq_3SEq_4 + SEq_1SEq_2) + twom_z * (0.5 - self.SEq_2 * self.SEq_2 - self.SEq_3 * self.SEq_3)

        # normalise the flux vector to have only components in the x and z
        self.b_x = math.sqrt((h_x * h_x) + (h_y * h_y))
        self.b_z = h_z
