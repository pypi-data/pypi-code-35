import numpy as np
from navipy.maths import quaternion as quat
from navipy.scene import is_numeric_array
import numbers
from navipy.maths.constants import _AXES2TUPLE

c = np.cos
s = np.sin


def R1(a):
    """ rotation matrix around the x- axis

    :param a: angle in degrees to be rotated
    :returns: a matrix
    :rtype: (np.ndarray)
    ..ref: James Diebel
           "Representing Attitude: Euler Angles, Unit Quaternions, and Rotation
           Vectors."
           (2006): p. 5 (2.4).
    """
    if not isinstance(a, numbers.Number):
        raise TypeError("angle must be numeric value")
    R1 = np.array([[1, 0, 0],
                   [0, c(a), s(a)],
                   [0, -s(a), c(a)]])
    return R1


def R2(a):
    """ rotation matrix around the y- axis

    :param a: angle in degrees to be rotated
    :returns: a matrix
    :rtype: (np.ndarray)
    ..ref: James Diebel
           "Representing Attitude: Euler Angles, Unit Quaternions, and Rotation
           Vectors."
           (2006): p. 5 (2.4).
    """
    if not isinstance(a, numbers.Number):
        raise TypeError("angle must be numeric value")
    R2 = np.array([[c(a), 0, -s(a)],
                   [0, 1, 0],
                   [s(a), 0, c(a)]])
    return R2


def R3(a):
    """ rotation matrix around the z- axis

    :param a: angle in degrees to be rotated
    :returns: a matrix
    :rtype: (np.ndarray)
    ..ref: James Diebel
           "Representing Attitude: Euler Angles, Unit Quaternions, and Rotation
           Vectors."
           (2006): p. 5 (2.4).
    """
    if not isinstance(a, numbers.Number):
        raise TypeError("angle must be numeric value")
    R3 = np.array([[c(a), s(a), 0],
                   [-s(a), c(a), 0],
                   [0, 0, 1]])
    return R3


def matrix(ai, aj, ak, axes='xyz'):
    """ rotation matrix around the three axis with the
        order given by the axes parameter

    :param ai: angle in degrees to be rotated about the first axis
    :param aj: angle in degrees to be rotated about the second axis
    :param ak: angle in degrees to be rotated about the third axis
    :returns: a matrix
    :rtype: (np.ndarray)
    ..ref: James Diebel
           "Representing Attitude: Euler Angles, Unit Quaternions, and Rotation
           Vectors."
           (2006): p. 9
    """
    if axes not in list(_AXES2TUPLE.keys()):
        raise ValueError("the chosen convention is not supported")
    r, i, j, k = _AXES2TUPLE[axes]
    matrixes = [R1, R2, R3]
    Rijk = np.dot(matrixes[i](ai),
                  np.dot(matrixes[j](aj),
                         matrixes[k](ak)))
    ID = np.identity(4)
    ID[:3, :3] = Rijk
    Rijk = ID
    return Rijk


def from_matrix(matrix, axes='xyz'):
    """Return Euler angles from rotation matrix for specified axis sequence.

    axes : One of 24 axis sequences as string or encoded tuple

    Note that many Euler angle triplets can describe one matrix.
    ..ref: James Diebel
           "Representing Attitude: Euler Angles, Unit Quaternions, and Rotation
           Vectors."
           (2006): p. 23 - 31.
    """
    if not isinstance(matrix, np.ndarray) and not isinstance(matrix, list):
        raise TypeError("matrix must be np.array or list")
    if axes not in list(_AXES2TUPLE.keys()):
        raise ValueError("the chosen convention is not supported")
    # if np.any(np.isnan(np.array(matrix, dtype=np.float64))):
    #    raise ValueError('posorient must not contain nan')
    if not is_numeric_array(matrix):
        raise ValueError("matrix must contain numeric values")
    if matrix.shape[0] > 3:
        matrix = matrix[:3, :3]
    u = None
    rot, i, j, k = _AXES2TUPLE[axes]
    #matrix = np.transpose(matrix)
    # if rot:
    #    matrix = np.transpose(matrix)
    #    new = list(axes)
    #    new[0] = 's'
    #    axes = ''.join(new)
    if axes == 'xyx':
        u = [np.arctan2(matrix[1, 0], matrix[2, 0]),
             np.arccos(matrix[0, 0]),
             np.arctan2(matrix[0, 1], -matrix[0, 2])]
    elif axes == 'xyz':
        u = [np.arctan2(matrix[1, 2], matrix[2, 2]),
             -np.arcsin(matrix[0, 2]),
             np.arctan2(matrix[0, 1], matrix[0, 0])]
    elif axes == 'xzx':
        u = [np.arctan2(matrix[2, 0], -matrix[1, 0]),
             np.arccos(matrix[0, 0]),
             np.arctan2(matrix[0, 2], matrix[0, 1])]
    elif axes == 'xzy':
        u = [np.arctan2(-matrix[2, 1], matrix[1, 1]),
             np.arcsin(matrix[0, 1]),
             np.arctan2(-matrix[0, 2], matrix[0, 0])]
    elif axes == 'yxy':
        u = [np.arctan2(matrix[0, 1], -matrix[2, 1]),
             np.arccos(matrix[1, 1]),
             np.arctan2(matrix[1, 0], matrix[1, 2])]
    elif axes == 'yxz':
        u = [np.arctan2(-matrix[0, 2], matrix[2, 2]),
             np.arcsin(matrix[1, 2]),
             np.arctan2(-matrix[1, 0], matrix[1, 1])]
    elif axes == 'yzx':
        u = [np.arctan2(matrix[2, 0], matrix[0, 0]),
             -np.arcsin(matrix[1, 0]),
             np.arctan2(matrix[1, 2], matrix[1, 1])]
    elif axes == 'yzy':
        u = [np.arctan2(matrix[2, 1], matrix[0, 1]),
             np.arccos(matrix[1, 1]),
             np.arctan2(matrix[1, 2], -matrix[1, 0])]
    elif axes == 'zxy':
        u = [np.arctan2(matrix[0, 1], matrix[1, 1]),
             -np.arcsin(matrix[2, 1]),
             np.arctan2(matrix[2, 0], matrix[2, 2])]
    elif axes == 'zxz':
        u = [np.arctan2(matrix[0, 2], matrix[1, 2]),
             np.arccos(matrix[2, 2]),
             np.arctan2(matrix[2, 0], -matrix[2, 1])]
    elif axes == 'zyx':
        u = [np.arctan2(-matrix[1, 0], matrix[0, 0]),
             np.arcsin(matrix[2, 0]),
             np.arctan2(-matrix[2, 1], matrix[2, 2])]
    elif axes == 'zyz':
        u = [np.arctan2(matrix[1, 2], -matrix[0, 2]),
             np.arccos(matrix[2, 2]),
             np.arctan2(matrix[2, 1], matrix[2, 0])]
    else:
        print("conv", axes, matrix)
        raise KeyError('convention not in {}', _AXES2TUPLE.keys())

    return u


def from_quaternion(quaternion, axes='xyz'):
    """Return Euler angles from quaternion for specified axis sequence.
    """
    if not isinstance(quaternion, np.ndarray) and\
       not isinstance(quaternion, list):
        raise TypeError("quaternions must be np.array or list")
    # if np.any(np.isnan(np.array(quaternion, dtype=np.float64))):
    #    raise ValueError('posorient must not contain nan')
    if axes not in list(_AXES2TUPLE.keys()):
        raise ValueError("the chosen convention is not supported")
    return from_matrix(quat.matrix(quaternion)[:3, :3], axes)


def angle_rate_matrix(ai, aj, ak, axes='xyz'):
    """
    Return the Euler Angle Rates Matrix

    from Diebels Representing Attitude: Euler Angles,
    Unit Quaternions, and Rotation, 2006
    rotation matrix around the three axis with the
        order given by the axes parameter

    :param ai: angle in degrees to be rotated about the first axis
    :param aj: angle in degrees to be rotated about the second axis
    :param ak: angle in degrees to be rotated about the third axis
    :param axes: string representation for the order of axes to be rotated
                 around and whether stationary or rotational
                 axes should be used
    :returns: a matrix
    :rtype: (np.ndarray)
    ..ref: James Diebel
           "Representing Attitude: Euler Angles, Unit Quaternions, and Rotation
           Vectors."
           (2006): p. 9 (5.2)
    """
    if not isinstance(ai, float) and not isinstance(ai, int):
        raise TypeError("euler angle must be of type float")
    if not isinstance(aj, float) and not isinstance(aj, int):
        raise TypeError("euler angle must be of type float")
    if not isinstance(ak, float) and not isinstance(ak, int):
        raise TypeError("euler angle must be of type float")
    # if np.isnan(np.array([ai], dtype=np.float64)) or\
    #   np.isnan(np.array([aj], dtype=np.float64)) or\
    #   np.isnan(np.array([ak], dtype=np.float64)):
    #    raise ValueError("quaternions must not be nan or none")
    if axes not in list(_AXES2TUPLE.keys()):
        raise ValueError("the chosen convention is not supported")
    _, i, j, k = _AXES2TUPLE[axes]
    ei = np.zeros(3)
    ej = np.zeros(3)
    ek = np.zeros(3)
    ei[i] = 1
    ej[j] = 1
    ek[k] = 1
    matrixes = [R1, R2, R3]
    Rj = matrixes[j](aj)
    Rj = np.transpose(Rj)
    Rk = matrixes[k](ak)
    Rk = np.transpose(Rk)
    p1 = np.dot(Rk, np.dot(Rj, ei))
    p2 = np.dot(Rk, ej)
    rotM = np.column_stack([p1, p2, ek])
    return rotM


def angular_velocity(ai, aj, ak, dai, daj, dak, axes='xyz'):
    """
    Return the angular velocity

    :param ai: angle in degrees to be rotated about the first axis
    :param aj: angle in degrees to be rotated about the second axis
    :param ak: angle in degrees to be rotated about the third axis
    :param dai: time derivative in degrees/time of the angle to be rotated
                about the first axis
    :param daj: time derivative in degrees/time of the angle to be rotated
                about the second axis
    :param dak: time derivative in degrees/time of the angle to be rotated
                about the third axis
    :param axes: string representation for the order of axes to be rotated
                 around and whether stationary or rotational axes should
                 be used
    :returns: a matrix
    :rtype: (np.ndarray)
    ..ref: James Diebel
           "Representing Attitude: Euler Angles, Unit Quaternions, and Rotation
           Vectors."
           (2006): p. 9 (5.2)
    """
    if not isinstance(ai, float) and not isinstance(ai, int):
        raise TypeError("euler angle must be of type float")
    if not isinstance(aj, float) and not isinstance(aj, int):
        raise TypeError("euler angle must be of type float")
    if not isinstance(ak, float) and not isinstance(ak, int):
        raise TypeError("euler angle must be of type float")
    if not isinstance(dai, float) and not isinstance(dai, int):
        raise TypeError("euler angle time derivative must be of type float")
    if not isinstance(daj, float) and not isinstance(daj, int):
        raise TypeError("euler angle time derivative must be of type float")
    if not isinstance(dak, float) and not isinstance(dak, int):
        raise TypeError("euler angle time derivative must be of type float")
    # if np.isnan(np.array([ai], dtype=np.float64)) or\
    #   np.isnan(np.array([aj], dtype=np.float64)) or\
    #   np.isnan(np.array([ak], dtype=np.float64)):
    #    raise ValueError("quaternions must not be nan or none")
    # if np.isnan(np.array([dai], dtype=np.float64)) or\
    #   np.isnan(np.array([daj], dtype=np.float64)) or\
    #   np.isnan(np.array([dak], dtype=np.float64)):
    #    raise ValueError("quaternions must not be nan or none")
    if axes not in list(_AXES2TUPLE.keys()):
        raise ValueError("the chosen convention is not supported")
    rotM = angle_rate_matrix(ai, aj, ak, axes)
    vel = np.dot(rotM, [dai, daj, dak])
    return vel
