"""
Numerical error propagation

tools to propogate the error by using an estimate
of the jacobian matrix (matrix of derivatives)
"""
import numpy as np


def estimate_error(markers, rigid_marker_id=[0, 1]):
    """
       Estimate the error by using the deviation from the median
distance between two markers
    """
    if not isinstance(rigid_marker_id, list):
        raise TypeError('rigid_marker_id should be a list')
    if len(rigid_marker_id) != 2:
        raise ValueError('rigid_marker_id should be a list with two elements')
    dist = np.sqrt(((markers.loc[:, rigid_marker_id[0]] -
                     markers.loc[:, rigid_marker_id[1]])**2).sum(
                         axis=1, skipna=False))
    median_dist = np.nanmedian(dist)
    return np.abs(dist - median_dist)


def estimate_jacobian(fun, x, args=None, epsilon=1e-6):
    """Estimate the jacobian matrix

    :param fun: The objective function to be derivated. Must be in \
the form f(x, *args). \
The argument, x, is a 1-D array of points, and args is a tuple of \
any additional \
fixed parameters needed to completely specify the function.
    :param x: values at which the jacobian should be calculated
    :param args: Extra arguments passed to the objective function
    :param epsilon: step used to estimate the jacobian
    :returns: An estimated jacobian matrix
    """
    if isinstance(x, (list, tuple, np.ndarray)):
        jacobian_matrix = list()
        for vari, _ in enumerate(x):
            x_minus = x.copy()
            x_plus = x.copy()
            x_minus[vari] -= epsilon
            x_plus[vari] += epsilon

            if args is None:
                dfs1 = fun(x_minus)
                dfs2 = fun(x_plus)
            else:
                dfs1 = fun(x_minus, args)
                dfs2 = fun(x_plus, args)
            dfs1 = np.array(dfs1)
            dfs2 = np.array(dfs2)
            deriv = (dfs2 - dfs1) / (2 * epsilon)
            jacobian_matrix.append(deriv)
        return np.array(jacobian_matrix).transpose()
    else:
        x_minus = x - epsilon
        x_plus = x + epsilon
        if args is None:
            deriv = (fun(x_plus) - fun(x_minus)) / (2 * epsilon)
        else:
            deriv = (fun(x_plus, args) - fun(x_minus, args)) / (2 * epsilon)
        return deriv


def propagate_error(fun, x, covar, args=None, epsilon=1e-6):
    """Estimate the jacobian matrix

    :param fun: The objective function to be error propagated. \
Must be in the form f(x, *args). \
The argument, x, is a 1-D array of points, and args is a tuple of \
any additional \
fixed parameters needed to completely specify the function.
    :param x: values at which the error should be calculated
    :param covar: variance-covariance matrix
    :param args: Extra arguments passed to the objective function
    :param epsilon: step used to estimate the jacobian
    :returns: An estimated jacobian matrix
    """
    jacobian_matrix = estimate_jacobian(fun, x, args, epsilon=1e-6)
    if isinstance(x, (list, tuple, np.ndarray)):
        return jacobian_matrix.dot(covar.dot(jacobian_matrix.transpose()))
    else:
        return np.abs(jacobian_matrix) * covar
