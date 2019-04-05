#===============================================================================
# allelicimbalance.py
#===============================================================================

"""Utilities for allelic imbalance analysis"""




# Imports ======================================================================

from betabernsum import bbs_cdf, bbs_test
from math import log2
from scipy.stats import beta




# Functions ====================================================================

def betabinom_test(
    x: int,
    n: int,
    a: float,
    b: float,
    alternative: str = 'two-sided',
    processes: int = 1
):
    """Perform a hypothesis test using a beta-binomial distribution

    Parameters
    ----------
    x : int
        number of successes
    n : int
        number of trials
    a : float
        first shape parameter
    b : float
        second shape parameter
    alternative : str
        alternative hypothesis {'less', 'greater', 'two-sided'}
    processes : int
        number of processes to use
    
    Returns
    -------
    float
        the p-value of the hypothesis test
    """

    return bbs_test(
        x, (n,), (a,), (b,), alternative=alternative, processes=processes
    )


def log_posterior_allelic_fold_change(
    c0: int,
    c1: int,
    a: float,
    b: float,
    level: float = 0.99
):
    """Bayesian effect size for imbalance data

    Parameters
    ----------
    c0 : int
        allele count 0
    c1 : int
        allele count 1
    a : float
        first shape parameter
    b : float
        second shape parameter
    level : float
        credibility level for credible interval

    Returns
    -------
    dict
       A dictionary with keys 'lpafc', 'lower', and 'upper'
    """

    posterior_mean = (a + c0) / (a + c0 + b + c1)
    posterior_mean_quantile = beta.cdf(posterior_mean, a + c0, b + c1)
    lower_prob = posterior_mean_quantile - level / 2
    upper_prob = posterior_mean_quantile + level / 2
    if (lower_prob > 0) and (upper_prob < 1):
        lower = beta.ppf(lower_prob, a + c0, b + c1)
        upper = beta.ppf(upper_prob, a + c0, b + c1)
    elif lower_prob > 0:
        lower = 0
        upper = beta.ppf(level, a + c0, b + c1)
    elif upper_prob < 1:
        lower = beta.ppf(1 - level, a + c0, b + c1)
        upper = 1
    shift_term = log2(a) - log2(b)
    return {
        'lpafc': log2(1 - posterior_mean) - log2(posterior_mean) + shift_term,
        'lower': float('-inf') if upper == 1 else log2(1 - upper) - log2(upper) + shift_term,
        'upper': float('inf') if lower == 0 else log2(1 - lower) - log2(lower) + shift_term
    }
