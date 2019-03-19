"""
Utilities
=============
Defines utility methods helpfull for working with ventana

"""

import numpy as np

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def get_indices(i, n):
    if i < 5:
        return list(range(0, min(i + 5, n)))
    elif i >= n - 5:
        return list(range(i - 5, n - 1))
    else:
        return list(range(i - 5, i + 5))

def vector_mag(x_vals, y_vals, z_vals):
    """
    Calculates vector magnitude from x, y, z raw tri-axial data

    :param x_vals: The x values
    :param y_vals: The y values
    :param z_vals: The z values
    :type x_vals: numpy array
    :type y_vals: numpy array
    :type z_vals: numpy array
    :return: List of vector magnitudes from sample x, y, z values
    :rtype: numpy array
    """
    full = np.stack([x_vals, y_vals, z_vals], axis = 1)
    return np.sqrt((full * full).sum(axis = 1))