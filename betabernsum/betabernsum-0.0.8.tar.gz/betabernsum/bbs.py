#===============================================================================
# bbs.py
#===============================================================================

# Imports ======================================================================

from functools import partial
from multiprocessing import Pool
from betabernsum.region import region
from betabernsum.probability_mass import (
    probability_mass_independent, probability_mass_dependent
)




# Functions ====================================================================

def bbs_pmf(k, n, a, b, independent=True):
    """Probability mass function for a sum of beta-bernoulli variables

    Parameters
    ----------
    k
        iterable giving the number of successes for each group
    n
        iterable giving the number of trials for each group
    a
        iterable giving the first shape parameter for each group
    b
        iterable giving the second shape parameter for each group
    independent : bool
        If TRUE (default), assume a sum of two independent groups of variables.
        If FALSE, assume all variables are mutually dependent.

    Returns
    -------
    float
        the value of the PMF
    """

    reg = region(k, n)
    return sum(
        probability_mass_independent(coord, n, a, b) if independent
        else probability_mass_dependent(coord, n, a, b)
        for coord in reg
    )

def bbs_cdf(k, n, a, b, independent=True, processes=1):
    """Cumulative distribution function for a sum of beta-bernoulli variables

    Parameters
    ----------
    k
        iterable giving the number of successes for each group
    n
        iterable giving the number of trials for each group
    a
        iterable giving the first shape parameter for each group
    b
        iterable giving the second shape parameter for each group
    independent : bool
        If TRUE (default), assume a sum of two independent groups of variables.
        If FALSE, assume all variables are mutually dependent.

    Returns
    -------
    float
        the value of the CDF
    """
    if processes == 1:
        return sum(
            map(
                partial(bbs_pmf, n=n, a=a, b=b, independent=independent),
                range(k + 1)
            )
        )
    else:
        with Pool(processes=processes) as pool:
            return sum(
                pool.map(
                    partial(bbs_pmf, n=n, a=a, b=b, independent=independent),
                    range(k + 1)
                )
            )
