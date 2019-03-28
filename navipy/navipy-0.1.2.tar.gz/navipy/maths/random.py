import numpy as np
from navipy.maths import quaternion as quat
from navipy.maths import constants
from navipy.maths.tools import unit_vector


def orthogonal_vectors():
    """ Generate two random vector, which are orthogonal
    """
    orthogonal = False
    while not orthogonal:
        vector_0 = np.random.random(3) - 0.5
        vector_1 = np.random.random(3) - 0.5
        normal = np.cross(vector_0, vector_1)
        vector_0_unit = unit_vector(vector_0)
        normal_unit = unit_vector(normal)
        orthogonal = abs(np.dot(normal_unit, vector_0_unit)
                         ) <= constants._EPS
    return vector_0, normal


def rotation_matrix(rand=None):
    """Return uniform random rotation matrix.

    rand: array like
            Three independent random variables that are uniformly distributed
            between 0 and 1 for each returned quaternion.
    """
    return quat.matrix(quaternion(rand))


def quaternion(rand=None):
    """Return uniform random unit quaternion.

    rand: array like or None
            Three independent random variables that are uniformly distributed
            between 0 and 1.
    """
    if rand is None:
        rand = np.random.rand(3)
    else:
        assert len(rand) == 3
    r1 = np.sqrt(1.0 - rand[0])
    r2 = np.sqrt(rand[0])
    pi2 = np.pi * 2.0
    t1 = pi2 * rand[1]
    t2 = pi2 * rand[2]
    return np.array([np.cos(t2) * r2, np.sin(t1) * r1,
                     np.cos(t1) * r1, np.sin(t2) * r2])
