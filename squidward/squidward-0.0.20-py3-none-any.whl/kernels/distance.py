"""
Distance functions to define how "far" apart two vectors are.
"""

import numpy as np
from squidward.utils import exactly_1d

np.seterr(over="raise")

class RBF(object):
    """Class for radial basis fucntion distance measure."""

    def __init__(self, lengthscale, var_k):
        """
        Description
        ----------
        Radial basis function (rbf) distance measure between vectors/arrays.

        Parameters
        ----------
        lengthscale: Float
            The lengthscale of the rbf function that detrmins the radius around
            which the value of an observation imapcts other observations.
        var_k: Float
            The kernel variance or amplitude. This can be thought of as the maximum
            value that the rbf function can take.

        Returns
        ----------
        distance object
        """
        self.lengthscale = lengthscale
        self.var_k = var_k
        if lengthscale <= 0.0:
            raise Exception("Lengthscale parameter must be greater than zero.")
        if var_k <= 0.0:
            raise Exception("Kernel variance parameter must be greater than zero.")

    def __call__(self, alpha, beta):
        """
        Radial basis function.
        """
        alpha, beta = exactly_1d(alpha), exactly_1d(beta)
        distance = np.sum((alpha - beta)**2)
        amp = -0.5/self.lengthscale**2
        return self.var_k*np.exp(amp*distance)
