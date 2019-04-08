"""This module implements a multivariate Gaussian distribution of a random vector
with INDEPENDENT ELEMENTS, i.e., diagonal covariance matrix,
and extends the scipy.stats implementations by including Bayesian learning.

This variant is a subclass where some mean values are forced == 0.,
to be used as a null model for hypothesis test and/or model comparisons

*** Classes:
GaussianNullRV: a trainable Gaussian distribution of a random vector with independent elements,
    subclass of gauss_gamma.GaussianRV

Arne Leijon, 2018-11-27
"""

import numpy as np
# from . import gauss_gamma

from PairedCompCalc import gauss_gamma  # needed only for TEST


# -------------------------------------------
class GaussianNullRV(gauss_gamma.GaussianRV):
    """Gaussian distribution of a random 1D (row) array with independent elements.
    Special adapt method forces some mean values to always remain at zero.
    """
    def __init__(self, n_null=0, **kwargs):
        """
        :param n_null: number of location elements to be kept at zero
        :param kwargs: (optional) keyword arguments to superclass
        """
        super().__init__(**kwargs)
        self.n_null = n_null
        self.mean.loc[:self.n_null] = 0.

    def adapt(self, x_source, prior):
        """Update distribution parameters using observed data and prior.
        :param x_source: iterable yielding samples (or list of samples) assumed drawn from self.
            NOTE: MUST allow several iteration rounds, so it cannot be a single iterator object.
        :param prior: prior conjugate distribution, same class as self
        :return: None
        Result: updated internal parameters of self
        Method: copied from superclass, only forcing some mean.loc elements -> 0.
        """
        m_samples = np.array([np.mean(x, axis=tuple(range(np.ndim(x) - 1)))
                              for x in x_source])
        # NOTE: each x MUST be 1D or 2D array or array-like list
        m_samples[..., :self.n_null] = 0.
        self.mean.adapt(m_samples, prior.mean)
        new_loc = self.mean.loc
        var_samples = [np.mean((x - new_loc)**2, axis=tuple(range(np.ndim(x) - 1)))
                       for x in x_source]
        self.prec.adapt(var_samples,
                        prior.prec,
                        prior.mean.learned_weight * (prior.mean.loc - new_loc)**2
                        )


# ------------------------------------------------- TEST
if __name__ == '__main__':
    from scipy.stats import norm
    # from scipy.stats import gamma
    import copy

    # --------------------------- Test PrecisionRV
    a = 10.
    b = [1.,2., 3.]
    nx= 10

    # --------------------------- Test GaussianRV
    g = GaussianNullRV(n_null=2, loc=[0.,1.,2.], scale=[1.,2.,3.], learned_weight=2.01)
    print(f'\n*** Testing {g}')
    print(f'g.var = \n{g.var}')
    # print(f'g.cov = \n{g.cov}')
    print(f'g.predictive.var = \n{g.predictive.var}')

    print('\n*** Learn GaussianNullRV from data:')

    # generative distribution:
    d = 3
    mu = np.array([1.,2.,3.])
    sd_within = np.array([3., 2., 1.])
    sd_between = 3.

    nx = 10  # number of independent "subjects"
    n_within = 100  # number of samples per subject
    y = sd_between * np.ones(d) * norm.rvs(size=(nx, 1, 1))
    x = mu + y + sd_within * norm.rvs(size=(nx, n_within, d))
    # theoretical mean(x) == mu; cov(x) = sd_between * ones((d,d)) + diag(sd_within)
    cov_within = np.diag(sd_within**2)
    cov_between = np.ones((d,d)) * sd_between**2
    cov_total = cov_between + cov_within
    print('mean_within = ', mu + y)
    print('mean_total = ', mu)
    print('cov_within =\n', cov_within)
    print('cov_between =\n', cov_between)
    print('cov_total =\n', cov_total)

    x_mean_total = np.mean(x, axis=(0,1))
    print(f'x_mean_total = {x_mean_total}')
    x_mean_within = np.mean(x, axis=1, keepdims=True)
    print('x_mean_within = \n', x_mean_within)

    dx = x - x_mean_within
    x_cov_within = np.einsum('nmi, nmj', dx, dx) / (nx * n_within)
    print('x_cov_within:\n', x_cov_within)

    dx = x - x_mean_total
    x_cov_total = np.einsum('nmi, nmj', dx, dx) / (nx * n_within)
    print('x_cov_total:\n', x_cov_total)

    gw0 = GaussianNullRV(n_null=2, loc=np.zeros(d), scale=np.ones(d), learned_weight=0.1)
    print('Prior GaussianNullRV:')
    print(gw0)

    gw = copy.deepcopy(gw0)
    gw.adapt(x, gw0)
    print('\nLearned GaussianNullRV:')
    print(gw)
    print('prec.mean:', gw.prec.mean)
    print('learned var:', gw.var)

    print('\nmean_logpdf(x[:,0,:])')
    print(gw.mean_logpdf(x[:,0,:]))

    print('\npredictive log pdf(x[:,0,:])')
    print(gw.predictive.logpdf(x[:,0,:]))


