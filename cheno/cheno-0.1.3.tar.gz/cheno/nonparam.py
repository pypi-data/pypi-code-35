from math import ceil, floor, sqrt

from scipy import stats
import numpy as np

from ._internal_utils import _gen_ranks_subsets
from .exceptions import IllegalArgumentError, OutOfBoundsError
from .utils import all_are_integers_or_none, count_none, gen_data_from_ranks


class MannWhitney(object):

    # TODO: Add ref. to effect size paper and to Andy Fields book
    @staticmethod
    def forward(x, y, use_continuity=True, alternative='two-sided'):
        """
        Compute the Mann-Whitney rank test on samples x and y.
        Parameters
        ----------
        x, y : array_like
            Array of samples, should be one-dimensional.
        use_continuity : bool, optional
                Whether a continuity correction (1/2.) should be taken into
                account. Default is True.
        alternative : None (deprecated), 'less', 'two-sided', or 'greater'
                Whether to get the p-value for the one-sided hypothesis ('less'
                or 'greater') or for the two-sided hypothesis ('two-sided').
                Defaults to None, which results in a p-value half the size of
                the 'two-sided' p-value and a different U statistic. The
                default behavior is not the same as using 'less' or 'greater':
                it only exists for backward compatibility and is deprecated.
        Returns
        -------
        ustatistic : float
            The Mann-Whitney U statistic, equal to min(U for x, U for y) if
            `alternative` is equal to None (deprecated; exists for backward
            compatibility), and U for y otherwise.
        zscore: float 
        pvalue : float
            p-value assuming an asymptotic normal distribution. One-sided or
            two-sided, depending on the choice of `alternative`.
        effectsize: float
            effect size, equal to the z-score divided to the square root of 
            total sample size
        Notes
        -----
        Use only when the number of observation in each sample is > 20 and
        you have 2 independent samples of ranks. Mann-Whitney U is
        significant if the u-obtained is LESS THAN or equal to the critical
        value of U.
        This test corrects for ties and by default uses a continuity correction.
        References
        ----------
        .. [1] https://en.wikipedia.org/wiki/Mann-Whitney_U_test
        .. [2] H.B. Mann and D.R. Whitney, "On a Test of Whether one of Two Random
            Variables is Stochastically Larger than the Other," The Annals of
            Mathematical Statistics, vol. 18, no. 1, pp. 50-60, 1947.
        """
        n1, n2 = len(x), len(y)
        u, p = stats.mannwhitneyu(
            x, y, use_continuity=use_continuity, alternative=alternative)
        z = (u - n1*n2/2) / (sqrt(n1*n2*(n1+n2+1) / 12))
        ef = z/sqrt(n1+n2)

        return u, z, p, ef

    # TODO: Add Docstring
    @staticmethod
    def inverse(p=.05, ef=.1, size=None, csize=[(5, 100), (5, 100)], tails=1, runs=1000, throw_err=True):
        if size is not None and ((len(size) == 2 and not all_are_integers_or_none(size)) or len(size) != 2):
            if throw_err:
                raise IllegalArgumentError(
                    f"Expecting integers for 'size' argument. You provided {size}.")

        size = [None, None]

        if tails not in [1, 2]:
            if throw_err:
                raise IllegalArgumentError(
                    f"Expecting either one or two tails. You provided {tails}.")
            else:
                tails = 1

        z = stats.norm.ppf(p / tails)
        size_total = int(round((z / ef) ** 2))

        # TODO: Check if size_total is inside permited bounds

        if count_none(size) == 0:
            if sum(size) != size_total:
                if throw_err:
                    raise IllegalArgumentError(
                        f"Sum of provided sample sizes has to match {size_total}, resulting from provided p-value={p} and number of tails {tails}.")
                else:
                    size = [None, None]

        if count_none(size) == 1:
            idx, n = ([(i, n) for i, n in enumerate(size) if n is not None])[0]
            size[1 - idx] = size_total - n
        else:
            size[0] = ceil(size_total / 2)
            size[1] = floor(size_total / 2)

        ranks = MannWhitney._inverse(z, size, runs)
        data = gen_data_from_ranks(ranks, size_total)

        return ranks, data

    @staticmethod
    def _inverse(z, size, runs):
        _w = min(size[0], size[1]) * (sum(size) + 1) / 2
        _se = sqrt(size[0] * size[1] * (sum(size) + 1) / 12)
        w = ceil(z * _se + _w)

        return _gen_ranks_subsets(size, w, runs)


class Friedman(object):

    
    @staticmethod
    def forward(*args):
        # TODO: Add Docstring
        F, p = stats.friedmanchisquare(*args)
        k = len(args)
        n = len(args[0])
        ef = F / (n*(k-1))

        return F, p, ef

    @staticmethod
    def inverse(p=.05, ef=.1, grps=4, size=None,
                csize=None, runs=1000, throw_err=True):
        # TODO: Add Docstring
        # TODO: Verify 'size' and 'csize'
        F = stats.chi2.ppf(1 - p, grps - 1)

        # TODO: Verify if 'size_total' is good value
        size_total = int(round((F / ef) / (grps - 1)))

        _F = ((F + 3 * size_total * (grps + 1)) / 12) * \
            (size_total * grps * (grps + 1))

        max_ss = sum([(size_total * x) ** 2 for x in range(1, grps + 1)])
        avg_ss = sum([(size_total * x) for x in range(1, grps + 1)]) / grps
        min_ss = []

        for i in range(1, grps + 1):
            if i % 2 == 0:
                min_ss.append(ceil(avg_ss))
            else:
                min_ss.append(floor(avg_ss))
        min_ss = sum([x ** 2 for x in min_ss])

        # TODO: Better Error Message
        if not min_ss <= _F <= max_ss:
            raise ValueError(
                "Impossible test statistics. Please try a different f-value.")

        ranks = Friedman._invers(_F, grps, size_total, runs)
        data = gen_data_from_ranks(ranks.T, size_total*grps)

        return ranks.T, data

    @staticmethod
    def _invers(F, grps, size_total, runs):

        def obj(x):
            s = [sum(x[:, i]) ** 2 for i in range(grps)]
            return sum(s) - F, sum(s), s

        ranks = np.array([list(range(1, grps + 1)) for _ in range(size_total)])
        min_diff, _, _ = obj(ranks)
        best_ranks = ranks.copy()

        for i in range(runs):
            m_ranks = np.copy(best_ranks)
            m_ranks[i % size_total] = np.random.permutation(
                m_ranks[i % size_total])
            d, _, _ = obj(m_ranks)

            if abs(d) < abs(min_diff):
                best_ranks = m_ranks
                min_diff = d

        return best_ranks
