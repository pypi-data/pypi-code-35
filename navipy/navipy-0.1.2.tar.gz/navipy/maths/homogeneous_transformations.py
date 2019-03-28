"""
"""
import numpy as np
from navipy.maths import constants
from navipy.maths import euler
from navipy.maths import quaternion
from navipy.maths.tools import vector_norm
from navipy.maths.tools import unit_vector


def translation_matrix(direction):
    """
    Return matrix to translate by direction vector
    """
    # get 4x4 identity matrix
    tmatrix = np.identity(4)
    # set the first three rows of the last colum to be the direction vector
    tmatrix[:3, 3] = direction[:3]
    return tmatrix


def translation_from_matrix(matrix):
    """
    Return translation vector from translation matrix
    """
    # returns the first three rows of the last colum in the rotation matrix
    return np.array(matrix, copy=False)[:3, 3].copy()


def reflection_matrix(point, normal):
    """
    Return matrix to mirror at plane defined by point and normal vector
    """
    # use only the first three columns of the normal vector
    normal = unit_vector(normal[:3])
    # get 4x4 identity matrix
    M = np.identity(4)
    # substract two times the outer product of the normal vector from the \
    # upper left 3x3 matrix of the unit matrix to
    M[:3, :3] -= 2.0 * np.outer(normal, normal)
    # set the fourth column of the resutlting matrix to 2* the dot product of \
    # the point and the normal vector times the noraml vector
    M[:3, 3] = (2.0 * np.dot(point[:3], normal)) * normal
    return M


def reflection_from_matrix(matrix):
    """Return mirror plane point and normal vector from reflection matrix.
    """
    # pointer to matrix (same as input)
    M = np.array(matrix, dtype=np.float64, copy=False)
    # normal: unit eigenvector corresponding to eigenvalue -1
    w, V = np.linalg.eig(M[:3, :3])
    # get eigenvectors with eigenvalue close to length 1 -> unit eigenvector; \
    # only for the upper left 3x3 part
    i = np.where(abs(np.real(w) + 1.0) < 1e-8)[0]
    if not len(i):
        raise ValueError("no unit eigenvector corresponding to eigenvalue -1")
    # choose only first of unit length eigenvectors
    normal = np.real(V[:, i[0]]).squeeze()
    # point: any unit eigenvector corresponding to eigenvalue 1
    # find eigenvector with unit length for whole matrix
    w, V = np.linalg.eig(M)
    i = np.where(abs(np.real(w) - 1.0) < 1e-8)[0]
    if not len(i):
        raise ValueError("no unit eigenvector corresponding to eigenvalue 1")
    # choose last of the unit length eigenvectors
    point = np.real(V[:, i[-1]]).squeeze()
    point /= point[3]
    return point, normal


def scale_matrix(factor, origin=None, direction=None):
    """Return matrix to scale by factor around origin in direction.
    Use factor -1 for point symmetry.
    """
    if direction is None:
        # uniform scaling
        M = np.diag([factor, factor, factor, 1.0])
        if origin is not None:
            M[:3, 3] = origin[:3]
            M[:3, 3] *= 1.0 - factor
    else:
        # nonuniform scaling
        direction = unit_vector(direction[:3])
        factor = 1.0 - factor
        M = np.identity(4)
        M[:3, :3] -= factor * np.outer(direction, direction)
        if origin is not None:
            M[:3, 3] = (factor * np.dot(origin[:3], direction)) * direction
    return M


def scale_from_matrix(matrix):
    """Return scaling factor, origin and direction from scaling matrix. """
    M = np.array(matrix, dtype=np.float64, copy=False)
    M33 = M[:3, :3]
    factor = np.trace(M33) - 2.0
    try:
        # direction: unit eigenvector corresponding to eigenvalue factor
        w, V = np.linalg.eig(M33)
        i = np.where(abs(np.real(w) - factor) < 1e-8)[0][0]
        direction = np.real(V[:, i]).squeeze()
        direction /= vector_norm(direction)
    except IndexError:
        # uniform scaling
        factor = (factor + 2.0) / 3.0
        direction = None
    # origin: any eigenvector corresponding to eigenvalue 1
    w, V = np.linalg.eig(M)
    i = np.where(abs(np.real(w) - 1.0) < 1e-8)[0]
    if not len(i):
        raise ValueError("no eigenvector corresponding to eigenvalue 1")
    origin = np.real(V[:, i[-1]]).squeeze()
    origin /= origin[3]
    return factor, origin, direction


def projection_matrix(point, normal, direction=None,
                      perspective=None, pseudo=False):
    """Return matrix to project onto plane defined by point and normal.

    Using either perspective point, projection direction, or none of both.

    If pseudo is True, perspective projections will preserve relative depth
    such that Perspective = dot(Orthogonal, PseudoPerspective).
    """
    M = np.identity(4)
    point = np.array(point[:3], dtype=np.float64, copy=False)
    normal = unit_vector(normal[:3])
    if perspective is not None:
        # perspective projection
        perspective = np.array(perspective[:3], dtype=np.float64,
                               copy=False)
        M[0, 0] = M[1, 1] = M[2, 2] = np.dot(perspective - point, normal)
        M[:3, :3] -= np.outer(perspective, normal)
        if pseudo:
            # preserve relative depth
            M[:3, :3] -= np.outer(normal, normal)
            M[:3, 3] = np.dot(point, normal) * (perspective + normal)
        else:
            M[:3, 3] = np.dot(point, normal) * perspective
        M[3, :3] = -normal
        M[3, 3] = np.dot(perspective, normal)
    elif direction is not None:
        # parallel projection
        direction = np.array(direction[:3], dtype=np.float64, copy=False)
        scale = np.dot(direction, normal)
        M[:3, :3] -= np.outer(direction, normal) / scale
        M[:3, 3] = direction * (np.dot(point, normal) / scale)
    else:
        # orthogonal projection
        M[:3, :3] -= np.outer(normal, normal)
        M[:3, 3] = np.dot(point, normal) * normal
    return M


def projection_from_matrix(matrix, pseudo=False):
    """Return projection plane and perspective point from projection matrix.

    Return values are same as arguments for projection_matrix function:
    point, normal, direction, perspective, and pseudo.
    """
    M = np.array(matrix, dtype=np.float64, copy=False)
    M33 = M[:3, :3]
    w, V = np.linalg.eig(M)
    i = np.where(abs(np.real(w) - 1.0) < 1e-8)[0]
    if not pseudo and len(i):
        # point: any eigenvector corresponding to eigenvalue 1
        point = np.real(V[:, i[-1]]).squeeze()
        point /= point[3]
        # direction: unit eigenvector corresponding to eigenvalue 0
        w, V = np.linalg.eig(M33)
        i = np.where(abs(np.real(w)) < 1e-8)[0]
        if not len(i):
            raise ValueError("no eigenvector corresponding to eigenvalue 0")
        direction = np.real(V[:, i[0]]).squeeze()
        direction /= vector_norm(direction)
        # normal: unit eigenvector of M33.T corresponding to eigenvalue 0
        w, V = np.linalg.eig(M33.T)
        i = np.where(abs(np.real(w)) < 1e-8)[0]
        if len(i):
            # parallel projection
            normal = np.real(V[:, i[0]]).squeeze()
            normal /= vector_norm(normal)
            return point, normal, direction, None, False
        else:
            # orthogonal projection, where normal equals direction vector
            return point, direction, None, None, False
    else:
        # perspective projection
        i = np.where(abs(np.real(w)) > 1e-8)[0]
        if not len(i):
            raise ValueError(
                "no eigenvector not corresponding to eigenvalue 0")
        point = np.real(V[:, i[-1]]).squeeze()
        point /= point[3]
        normal = - M[3, :3]
        perspective = M[:3, 3] / np.dot(point[:3], normal)
        if pseudo:
            perspective -= normal
        return point, normal, None, perspective, pseudo


def shear_matrix(angle, direction, point, normal):
    """Return matrix to shear by angle along direction vector on shear plane.

    The shear plane is defined by a point and normal vector. The direction
    vector must be orthogonal to the plane's normal vector.

    A point P is transformed by the shear matrix into P" such that
    the vector P-P" is parallel to the direction vector and its extent is
    given by the angle of P-P'-P", where P' is the orthogonal projection
    of P onto the shear plane.
    """
    normal = unit_vector(normal[:3])
    direction = unit_vector(direction[:3])
    if abs(np.dot(normal, direction)) > constants._EPS:
        raise ValueError("direction and normal vectors are not orthogonal")
    angle = np.tan(angle)
    M = np.identity(4)
    M[:3, :3] += angle * np.outer(direction, normal)
    M[:3, 3] = -angle * np.dot(point[:3], normal) * direction
    return M


def shear_from_matrix(matrix):
    """Return shear angle, direction and plane from shear matrix.
    """
    M = np.array(matrix, dtype=np.float64, copy=False)
    M33 = M[:3, :3]
    # normal: cross independent eigenvectors corresponding to the eigenvalue 1
    w, V = np.linalg.eig(M33)
    i = np.where(abs(np.real(w) - 1.0) < 1e-4)[0]
    if len(i) < 2:
        raise ValueError("no two linear independent eigenvectors found %s" % w)
    V = np.real(V[:, i]).squeeze().T
    lenorm = -1.0
    for i0, i1 in ((0, 1), (0, 2), (1, 2)):
        n = np.cross(V[i0], V[i1])
        w = vector_norm(n)
        if w > lenorm:
            lenorm = w
            normal = n
    normal /= lenorm
    # direction and angle
    direction = np.dot(M33 - np.identity(3), normal)
    angle = vector_norm(direction)
    direction /= angle
    angle = np.arctan(angle)
    # point: eigenvector corresponding to eigenvalue 1
    w, V = np.linalg.eig(M)
    i = np.where(abs(np.real(w) - 1.0) < 1e-8)[0]
    if not len(i):
        raise ValueError("no eigenvector corresponding to eigenvalue 1")
    point = np.real(V[:, i[-1]]).squeeze()
    point /= point[3]
    return angle, direction, point, normal


def decompose_matrix(matrix, axes='xyz'):
    """Return sequence oftransformations from transformation matrix.

    matrix : array_like
            Non-degenerative homogeneous transformation matrix

    Return tuple of:
            scale : vector of 3 scaling factors
            shear : list of shear factors for x-y, x-z, y-z axes
            angles : list of Euler angles about static x, y, z axes
            translate : translation vector along x, y, z axes
            perspective : perspective partition of matrix

    Raise ValueError if matrix is of wrong type or degenerative.
    """
    M = np.array(matrix, dtype=np.float64, copy=True).T
    if abs(M[3, 3]) < constants._EPS:
        raise ValueError("M[3, 3] is zero")
    M /= M[3, 3]
    P = M.copy()
    P[:, 3] = 0.0, 0.0, 0.0, 1.0
    if not np.linalg.det(P):
        raise ValueError("matrix is singular")

    scale = np.zeros((3, ))
    shear = [0.0, 0.0, 0.0]
    angles = [0.0, 0.0, 0.0]

    if any(abs(M[:3, 3]) > constants._EPS):
        perspective = np.dot(M[:, 3], np.linalg.inv(P.T))
        M[:, 3] = 0.0, 0.0, 0.0, 1.0
    else:
        perspective = np.array([0.0, 0.0, 0.0, 1.0])

    translate = M[3, :3].copy()
    M[3, :3] = 0.0

    row = M[:3, :3].copy()
    scale[0] = vector_norm(row[0])
    row[0] /= scale[0]
    shear[0] = np.dot(row[0], row[1])
    row[1] -= row[0] * shear[0]
    scale[1] = vector_norm(row[1])
    row[1] /= scale[1]
    shear[0] /= scale[1]
    shear[1] = np.dot(row[0], row[2])
    row[2] -= row[0] * shear[1]
    shear[2] = np.dot(row[1], row[2])
    row[2] -= row[1] * shear[2]
    scale[2] = vector_norm(row[2])
    row[2] /= scale[2]
    shear[1:] /= scale[2]

    if np.dot(row[0], np.cross(row[1], row[2])) < 0:
        np.negative(scale, scale)
        np.negative(row, row)

    mat = np.linalg.inv(row[:3, :3])
    angles = euler.from_matrix(mat, axes)
    return scale, shear, angles, translate, perspective


def compose_matrix(scale=None, shear=None, angles=None, translate=None,
                   perspective=None, axes='xyz'):
    """Return transformation matrix from sequence oftransformations.

    This is the inverse of the decompose_matrix function.

    Sequence of transformations:
            scale : vector of 3 scaling factors
            shear : list of shear factors for x-y, x-z, y-z axes
            angles : list of Euler angles about static x, y, z axes
            translate : translation vector along x, y, z axes
            perspective : perspective partition of matrix
    """
    M = np.identity(4)
    if perspective is not None:
        P = np.identity(4)
        P[3, :] = perspective[:4]
        M = np.dot(M, P)
    if translate is not None:
        T = np.identity(4)
        T[:3, 3] = translate[:3]
        M = np.dot(M, T)
    if angles is not None:
        if axes == 'quaternion':
            R = quaternion.matrix(angles)
        else:
            R = euler.matrix(angles[0], angles[1], angles[2], axes)
        M = np.dot(M, R)
    if shear is not None:
        Z = np.identity(4)
        Z[1, 2] = shear[2]
        Z[0, 2] = shear[1]
        Z[0, 1] = shear[0]
        M = np.dot(M, Z)
    if scale is not None:
        S = np.identity(4)
        S[0, 0] = scale[0]
        S[1, 1] = scale[1]
        S[2, 2] = scale[2]
        M = np.dot(M, S)
    M /= M[3, 3]
    return M


def is_same_transform(matrix0, matrix1):
    """Return True if two matrices perform same transformation.
    """
    matrix0 = np.array(matrix0, dtype=np.float64, copy=True)
    matrix0 /= matrix0[3, 3]
    matrix1 = np.array(matrix1, dtype=np.float64, copy=True)
    matrix1 /= matrix1[3, 3]
    return np.allclose(matrix0, matrix1)


def testing_is_same_transform(matrix0, matrix1):
    """Return True if two matrices perform same transformation.
    """
    matrix0 = np.array(matrix0, dtype=np.float64, copy=True)
    matrix0 /= matrix0[3, 3]
    matrix1 = np.array(matrix1, dtype=np.float64, copy=True)
    matrix1 /= matrix1[3, 3]
    np.testing.assert_allclose(matrix0, matrix1)
