"""
"""
import numpy as np


def vector_norm(data, axis=0):
    """Return Euclidean norm of ndarray along axis.
    """
    if isinstance(data, list):
        data = np.array(data)
    assert isinstance(data, np.ndarray), 'data should be a numpy array'

    return np.sqrt(np.sum(data * data, axis=axis, keepdims=True))


def unit_vector(data, axis=0):
    """Return ndarray normalized by length, i.e. Euclidean norm, along axis.
    """
    if isinstance(data, list):
        data = np.array(data)

    assert isinstance(data, np.ndarray), 'data should be a numpy array'
    repetitions = np.array(data.shape)
    repetitions[:] = 1
    repetitions[axis] = data.shape[axis]
    norm = vector_norm(data, axis)
    return data / np.tile(norm, repetitions)


def angle_between_vectors(vector_0, vector_1, directed=True, axis=0):
    """Return angle between vectors.

    If directed is False, the input vectors are interpreted as undirected axes,
    i.e. the maximum angle is pi/2.
    """
    vector_0 = np.array(vector_0, dtype=np.float64, copy=False)
    vector_1 = np.array(vector_1, dtype=np.float64, copy=False)
    dot = np.sum(vector_0 * vector_1, axis=axis, keepdims=True)
    dot /= vector_norm(vector_0, axis=axis) \
        * vector_norm(vector_1, axis=axis)
    dot = np.squeeze(dot)
    return np.arccos(dot if directed else np.fabs(dot))


def inverse_matrix(matrix):
    """Return inverse of square transformation matrix.
    """
    return np.linalg.inv(matrix)


def concatenate_matrices(*matrices):
    """Return concatenation of series of transformation matrices.
    """
    M = np.identity(4)
    for i in matrices:
        M = np.dot(M, i)
    return M

