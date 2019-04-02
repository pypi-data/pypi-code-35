"""
This script contains code for basic gaussian process regression. A regression
model can be created by calling one of these classes to create a model object.
"""

import numpy as np
from squidward.utils import Invert, exactly_2d, check_valid_cov

np.seterr(over="raise")

class GaussianProcess(object):
    """Model object for single output gaussian process (SOGP) regression."""

    def __init__(self, kernel=None, var_l=1e-15, inv_method="inv"):
        """
        Description
        ----------
        Model object for single output gaussian process (SOGP) regression.

        Parameters
        ----------
        kernel : kernel object
            An object with an associated function k that takes in 2 arrays and
            returns a valid K matrix. Valid K matricies are positive
            semi-definite and not singular.
        var_l: float
            The liklihood variance of the process. Currently only supports
            scalars for homoskedastic regression.
        inv_method: string
            A string argument choosing an inversion method for matrix K when
            fitting the gaussian process.

        Returns
        ----------
        Model object
        """
        self.kernel = kernel
        self.var_l = var_l
        self.x_obs = None
        self.y_obs = None
        self.inv = Invert(inv_method)
        self.K = None
        self.fitted = False
        assert self.kernel is not None, \
            "Model object must be instantiated with a valid kernel object."
        assert self.var_l >= 0.0, \
            "Invalid likelihood variance argument."

    def fit(self, x_obs, y_obs):
        """
        Description
        ----------
        Fit the model to data. This function takes in training data
        (x: features, y: targets) and fits the K matrix to that data. The
        predict function can then be used to make predictions.

        Parameters
        ----------
        x_obs: array_like
            An array containing the model features.
        y_obs: array_like
            An array containing the model targets (currently only supports
            single outputs).

        Returns
        ----------
        None
        """
        self.x_obs = exactly_2d(x_obs)
        self.y_obs = exactly_2d(y_obs)
        K = self.kernel(x_obs, x_obs)

        identity = np.zeros(K.shape)
        idx = np.diag_indices(identity.shape[0])
        identity[idx] = self.var_l
        K += identity

        self.K = self.inv(K)
        self.fitted = True

    def posterior_predict(self, x_test, return_cov=False):
        """
        Description
        ----------
        Make predictions based on fitted model. This function takes in a set of
        test points to make predictions on and returns the mean function of the
        gaussian process and a measure of uncertainty (either covariance or
        variance).

        Parameters
        ----------
        x_test: array_like
            Feature input for points to make predictions for.
        return_cov: boolean
            If true, will return the full covariance matrix. Otherwise it will
            return the variance.

        Returns
        ----------
        Mean: array_like
            An array with the values of the mean function of the guassian
            process posterior.
        Var: array_like
            The variance around the values of the mean function of the
            gaussian process posterior.
        Cov: array_like
            The full covariance matrix opf the gaussian process posterior.
        """
        assert self.fitted and (self.K is not None), "Please fit the model before trying to make posterior predictions!"

        # Gaussian Processes for Machine Learning Eq 2.18/2.19
        K_s = self.kernel(x_test, self.x_obs)
        mean = K_s.dot(self.K).dot(self.y_obs)
        K_ss = self.kernel(x_test, x_test)
        cov = K_ss - np.dot(np.dot(K_s, self.K), K_s.T)
        check_valid_cov(cov)
        if return_cov:
            return mean, cov
        var = exactly_2d(np.diag(cov))
        return mean, var

    def prior_predict(self, x_test, return_cov=False):
        """
        Description
        ----------
        Make predictions. This function takes in a set of test points to make
        predictions on and returns the mean function of the prior of the
        gaussian process and a measure of uncertainty (either covariance or
        variance).

        Parameters
        ----------
        x_test: array_like
            Feature input for points to make predictions for.
        return_cov: boolean
            If true, will return the full covariance matrix. Otherwise it will
            return the variance.

        Returns
        ----------
        Mean: array_like
            An array with the values of the mean function of the guassian
            process prior.
        Var: array_like
            The variance around the values of the mean function of the
            gaussian process prior.
        Cov: array_like
            The full covariance matrix opf the gaussian process prior.
        """
        # update to take into account constant kernels
        mean = np.zeros(x_test.shape[0]).reshape(-1, 1)
        cov = self.kernel(x_test, x_test)

        check_valid_cov(cov)
        if return_cov:
            return mean, cov
        var = exactly_2d(np.diag(cov))
        return mean, var

    def posterior_sample(self, x_test):
        """
        Description
        ----------
        Draw a function from the fitted posterior.

        Parameters
        ----------
        x_test: array_like
            Feature input for points to draw samples for.

        Returns
        ----------
        Sample: array_like
            The values of a function sampled from the gaussian process posterior.
        """
        assert self.fitted, "Please fit the model before trying to make posterior predictions!"

        mean, cov = self.posterior_predict(x_test, True)
        check_valid_cov(cov)
        return np.random.multivariate_normal(mean[:, 0], cov, 1).T[:, 0]

    def prior_sample(self, x_test):
        """
        Description
        ----------
        Draw a function from the prior.

        Parameters
        ----------
        x_test: array_like
            Feature input for points to draw samples for.

        Returns
        ----------
        Sample: array_like
            The values of a function sampled from the gaussian process prior.
        """
        mean, cov = self.prior_predict(x_test, True)
        check_valid_cov(cov)
        return np.random.multivariate_normal(mean[:, 0], cov, 1).T[:, 0]

class GaussianProcessStableCholesky(object):
    """Model object for single output gaussian process (SOGP) regression formulated for stability.."""

    def __init__(self, kernel=None, var_l=1e-15):
        """
        Description
        ----------
        Model object for single output gaussian process (SOGP) regression using
        algorithm 2.1 (pg.19) from Gaussian Processes for Machine Learning
        for increased numerical stability and faster performance.

        Parameters
        ----------
        kernel : kernel object
            An object with an associated function k that takes in 2 arrays and
            returns a valid K matrix. Valid K matricies are positive
            semi-definite and not singular.
        var_l: float
            The liklihood variance of the process. Currently only supports
            scalars for homoskedastic regression.

        Returns
        ----------
        Model object
        """
        self.kernel = kernel
        self.var_l = var_l
        assert self.kernel is not None, \
            "Model object must be instantiated with a valid kernel object."
        assert self.var_l >= 0.0, \
            "Invalid likelihood variance argument."

    def fit_predict(self, x_obs, y_obs, x_test, return_cov=False):
        """
        Description
        ----------
        Model object for single output gaussian process (SOGP) regression. This
        object uses algorithm 2.1 (pg.19) from Gaussian Processes for Machine
        Learning for increased numerical stability and faster performance.

        Parameters
        ----------
        x_obs: array_like
            An array containing the model features.
        y_obs: array_like
            An array containing the model targets (currently only supports
            single outputs - SOGP).
        x_test: array_like
            Feature input for points to make predictions for.
        kernel : kernel object
            An object with an associated function k that takes in 2 arrays and
            returns a valid K matrix. Valid K matricies are positive
            semi-definite and not singular.
        var_l: float
            The liklihood variance of the process. Currently only supports
            scalars for homoskedastic regression.
        return_cov: boolean
            If true, will return the full covariance matrix. Otherwise it will
            return the variance.

        Returns
        ----------
        Mean: array_like
            An array with the values of the mean function of the guassian
            process posterior.
        Var: array_like
            The variance around the values of the mean function of the
            gaussian process posterior.
        Cov: array_like
            The full covariance matrix opf the gaussian process posterior.
        """

        x_obs = exactly_2d(x_obs)
        y_obs = exactly_2d(y_obs)

        # Gaussian Processes for Machine Learning Eq 2.18/2.19
        K = self.kernel(x_obs, x_obs)
        K_ = self.kernel(x_obs, x_test)
        K_ss = self.kernel(x_test, x_test)

        identity = np.zeros(K.shape)
        idx = np.diag_indices(identity.shape[0])
        identity[idx] = self.var_l
        K += identity

        # More numerically stable
        # Gaussian Processes for Machine Learning Alg 2.1
        L = np.linalg.cholesky(K)
        alpha = np.linalg.solve(L.transpose(), np.linalg.solve(L, y_obs))
        V = np.linalg.solve(L, K_)
        mean = np.dot(K_.transpose(), alpha)
        cov = K_ss - np.dot(V.transpose(), V)
        check_valid_cov(cov)
        if return_cov:
            return mean, cov
        var = exactly_2d(np.diag(cov))
        return mean, var
