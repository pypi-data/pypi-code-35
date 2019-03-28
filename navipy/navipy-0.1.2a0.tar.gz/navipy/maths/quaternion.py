"""


"""
import numpy as np
from navipy.maths import constants
from navipy.maths.tools import vector_norm


def qat(a, n):
    """ axis-angle quaternion function
    Returns a unit quaternion

    :param a: angle in degrees
    :param n: unit canonical vector for a specific axis
    :returns: a vector
    :rtype: (np.ndarray)
    ..ref: James Diebel
           "Representing Attitude: Euler Angles, Unit Quaternions, and Rotation
           Vectors."
           (2006): p. 17 (6.12)
    """
    tmp = np.zeros((4))
    tmp[0] = np.cos((1 / 2) * a)
    tmp[1:4] = np.dot(n, np.sin((1 / 2) * a))
    return tmp


def from_euler(ai, aj, ak, axes='xyz'):
    """Return quaternion from Euler angles and axis sequence.
    ai, aj, ak : Euler's roll, pitch and yaw angles
    axes : One of 24 axis sequences as string or encoded tuple
    :param ai: angle in degrees to be rotated about the first axis
    :param aj: angle in degrees to be rotated about the second axis
    :param ak: angle in degrees to be rotated about the third axis
    :param axes: string that encodes the order of the axes and
                 whether rotational or stationary axes should be used
    :returns: a vector
    :rtype: (np.ndarray)
    ..ref: James Diebel
           "Representing Attitude: Euler Angles, Unit Quaternions, and Rotation
           Vectors."
           (2006): p. 18 (6.14)
    """
    vects = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    r, i, j, k = constants._AXES2TUPLE[axes]
    q1 = qat(ai, vects[i])
    q2 = qat(aj, vects[j])
    q3 = qat(ak, vects[k])
    quaternion = multiply(np.array(q1), np.array(q2))
    qijk = multiply(quaternion, np.array(q3))
    return qijk


def about_axis(angle, axis):
    """Return quaternion for rotation about axis.

    ..ref: James Diebel
           "Representing Attitude: Euler Angles, Unit Quaternions, and Rotation
           Vectors."
           (2006): p. 17 (6.4), equation 175
    """
    q = np.array([0.0, axis[0], axis[1], axis[2]])
    qlen = vector_norm(q)
    if qlen > constants._EPS:
        q *= np.sin(angle / 2.0) / qlen
    q[0] = np.cos(angle / 2.0)
    return q


def matrix(quaternion):
    """Return homogeneous rotation matrix from quaternion.
    :param quaternion : vector with at least 3 entrences (unit quaternion)
    :returns: a matrix
    :rtype: (np.ndarray)
    ..ref: James Diebel
           "Representing Attitude: Euler Angles, Unit Quaternions, and Rotation
           Vectors."
           (2006): p. 15 (6.4)
    """
    q = np.array(quaternion, dtype=np.float64, copy=True)
    qnorm = np.sqrt(q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2)
    if qnorm != 1:
        q = q / qnorm
    q0 = q[0]
    q1 = q[1]
    q2 = q[2]
    q3 = q[3]

    mat = np.identity(4)
    # According to equation 125
    mat[:3, :3] = np.array([
        [q0**2 + q1**2 - q2**2 - q3**2, 2 * q1 * q2 +
            2 * q0 * q3, 2 * q1 * q3 - 2 * q0 * q2],
        [2 * q1 * q2 - 2 * q0 * q3, q0**2 - q1**2 +
            q2**2 - q3**2, 2 * q2 * q3 + 2 * q0 * q1],
        [2 * q1 * q3 + 2 * q0 * q2, 2 * q2 * q3 - 2 * q0 * q1, q0**2 - q1**2 - q2**2 + q3**2]])
    return mat


def from_matrix(matrix):
    """Return quaternion from rotation matrix.

    :param matrix: a rotation matrix
    :returns: a vector
    :rtype: (np.ndarray)
    ..ref: James Diebel
           "Representing Attitude: Euler Angles, Unit Quaternions, and Rotation
           Vectors."
           (2006): p. 15 (6.5)
    """
    r = matrix
    # Split cases according to equation 145
    if (r[1, 1] >= -r[2, 2]) and (r[0, 0] >= -r[1, 1]) and (r[0, 0] >= -r[2, 2]):
        # equation 141
        return (1 / 2) * np.array([np.sqrt(1 + r[0, 0] + r[1, 1] + r[2, 2]),
                                   (r[1, 2] - r[2, 1]) /
                                   np.sqrt(1 + r[0, 0] + r[1, 1] + r[2, 2]),
                                   (r[2, 0] - r[0, 2]) /
                                   np.sqrt(1 + r[0, 0] + r[1, 1] + r[2, 2]),
                                   (r[0, 1] - r[1, 0]) /
                                   np.sqrt(1 + r[0, 0] + r[1, 1] + r[2, 2])])

    if (r[1, 1] < -r[2, 2]) and (r[0, 0] > r[1, 1]) and (r[0, 0] > r[2, 2]):
        # equation 142
        return (1 / 2) * np.array([(r[1, 2] - r[2, 1]) /
                                   np.sqrt(1 + r[0, 0] - r[1, 1] - r[2, 2]),
                                   np.sqrt(1 + r[0, 0] - r[1, 1] - r[2, 2]),
                                   (r[0, 1] + r[1, 0]) /
                                   np.sqrt(1 + r[0, 0] - r[1, 1] - r[2, 2]),
                                   (r[2, 0] + r[0, 2]) /
                                   np.sqrt(1 + r[0, 0] - r[1, 1] - r[2, 2])])
    if (r[1, 1] > r[2, 2]) and (r[0, 0] < r[1, 1]) and (r[0, 0] < -r[2, 2]):
        # equation 143
        return (1 / 2) * np.array([(r[2, 0] - r[0, 2]) /
                                   np.sqrt(1 - r[0, 0] + r[1, 1] - r[2, 2]),
                                   (r[0, 1] + r[1, 0]) /
                                   np.sqrt(1 - r[0, 0] + r[1, 1] - r[2, 2]),
                                   np.sqrt(1 - r[0, 0] + r[1, 1] - r[2, 2]),
                                   (r[1, 2] + r[2, 1]) /
                                   np.sqrt(1 - r[0, 0] + r[1, 1] - r[2, 2])])
    if (r[1, 1] < r[2, 2]) and (r[0, 0] < -r[1, 1]) and (r[0, 0] < r[2, 2]):
        # equation 144
        return (1 / 2) * np.array([(r[0, 1] - r[1, 0]) /
                                   np.sqrt(1 - r[0, 0] - r[1, 1] + r[2, 2]),
                                   (r[2, 0] + r[0, 2]) /
                                   np.sqrt(1 - r[0, 0] - r[1, 1] + r[2, 2]),
                                   (r[1, 2] + r[2, 1]) /
                                   np.sqrt(1 - r[0, 0] - r[1, 1] + r[2, 2]),
                                   np.sqrt(1 - r[0, 0] - r[1, 1] + r[2, 2])])


def multiply(quaternion1, quaternion0):
    """Return multiplication of two quaternions.
    """
    w0, x0, y0, z0 = quaternion0
    w1, x1, y1, z1 = quaternion1
    return np.array([-x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0,
                     x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0,
                     -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0,
                     x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0], dtype=np.float64)


def conjugate(quaternion):
    """Return conjugate of quaternion.
    """
    q = np.array(quaternion, dtype=np.float64, copy=True)
    np.negative(q[1:], q[1:])
    return q


def inverse(quaternion):
    """Return inverse of quaternion.
    """
    q = np.array(quaternion, dtype=np.float64, copy=True)
    np.negative(q[1:], q[1:])
    return q / np.dot(q, q)


def real(quaternion):
    """Return real part of quaternion.
    """
    return float(quaternion[0])


def imag(quaternion):
    """Return imaginary part of quaternion.
    """
    return np.array(quaternion[1:4], dtype=np.float64, copy=True)


def diff(quaternion0, quaternion1):
    """ The axis and angle between two quaternions
    """
    q = multiply(quaternion1, conjugate(quaternion0))
    length = np.sum(np.sqrt(q[1:4] * q[1:4]))
    angle = 2 * np.arctan2(length, q[0])
    if np.isclose(length, 0):
        axis = np.array([1, 0, 0])
    else:
        axis = q[1:4] / length
    return axis, angle
