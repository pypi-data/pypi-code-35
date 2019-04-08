"""Numerically safer version of scipy.stats.logistic distribution,
avoiding numerical overflow.
May be replaced by future improved version of scipy.stats.logistic.

Arne Leijon, 2017-03-13
"""
import numpy as np
from scipy.stats import rv_continuous
from scipy.special import expit, logit


class logistic_gen(rv_continuous):
    """Safer version with central METHODS re-implemented.
    Function interface copied from scipy.stats.logistic_gen
    """
    def _logpdf(self, x):
        """pdf(x) = exp(-x)/(1+exp(-x))**2
        logpdf(x) = -x - 2 * log((1+exp(-x))
        This is fine for large positive x, but pdf is symmetric,
        so we use abs(x) to avoid overflow for large negative x.
        """
        nax = - np.abs(x)
        return nax - 2. * np.log1p(np.exp(nax))

    def _logcdf(self, x):
        """log logistic.cdf = -log( 1 + exp(-x) )
        = -x - log(1 + exp(x)), for x < 0.
        safer than scipy.stats.logistic.logcdf
        Input:
        x = array of input variables
        """
        x = np.asarray(x)
        ax = np.abs(x)
        lP = - np.log1p(np.exp(-ax))
        negx = x < 0
        lP[negx] -= ax[negx]
        return lP

    # ----------------------------------------------------
    # following private METHODS copied from scipy.stats.logistic_gen

    def _rvs(self):
        return self._random_state.logistic(size=self._size)

    def _pdf(self, x):
        return np.exp(self._logpdf(x))

    def _cdf(self, x):
        return expit(x)

    def _ppf(self, q):
        return logit(q)

    def _sf(self, x):
        return expit(-x)

    def _isf(self, q):
        return - logit(q)

    def _stats(self):
        return 0, np.pi * np.pi / 3.0, 0, 6.0 / 5.0

    def _entropy(self):
        # http://en.wikipedia.org/wiki/Logistic_distribution
        return 2.0
# ---------------------------------------------------------


logistic = logistic_gen(name='logistic')


# --------------------------------------------------------- TEST:
if __name__ == '__main__':
    from scipy.stats import logistic as sc_logistic

    x = np.array([0., 2., 1000., np.inf])

    print('x= ', x)
    print('\nImproved logistic version:')
    print('logistic.logpdf(x) = ', logistic.logpdf(x))
    print('logistic.logpdf(-x)= ', logistic.logpdf(-x))
    print('logistic.pdf(x) = ', logistic.pdf(x))
    print('logistic.pdf(-x)= ', logistic.pdf(-x))
    print('logistic.cdf(x) = ', logistic.cdf(x))
    print('logistic.cdf(-x)= ', logistic.cdf(-x))
    print('logistic.logcdf(x) = ', logistic.logcdf(x))
    print('logistic.logcdf(-x)= ', logistic.logcdf(-x))
    print('logistic.ppf(cdf(x)) = ', logistic.ppf(logistic.cdf(x)))
    print('logistic.ppf(cdf(-x))= ', logistic.ppf(logistic.cdf(-x)))

    print('logistic.pdf(x, loc=2.)', logistic.pdf(x, loc=2.))
    print('logistic.logcdf(x, scale=0.02)', logistic.logcdf(x, scale=0.02))

    print('logistic.rvs(size=10)', logistic.rvs(size=10))

    print('')
    print('scipy.stats version:')
    print('scipy.stats.logistic.logpdf(x) = ', sc_logistic.logpdf(x))
    print('scipy.stats.logistic.logpdf(-x)= ', sc_logistic.logpdf(-x))
    print('scipy.stats.logistic.logcdf(x) = ', sc_logistic.logcdf(x))
    print('scipy.stats.logistic.logcdf(-x)= ', sc_logistic.logcdf(-x))


