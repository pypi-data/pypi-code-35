"""
The :mod:`h2o4gpu.mixture` module implements mixture modeling algorithms.
"""

from .gaussian_mixture import GaussianMixture
from .bayesian_mixture import BayesianGaussianMixture


__all__ = ['GaussianMixture',
           'BayesianGaussianMixture']
