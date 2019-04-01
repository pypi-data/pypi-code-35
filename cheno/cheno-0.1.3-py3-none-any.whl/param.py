import multiprocessing as mp
from itertools import product
from math import isclose, sqrt

import numpy as np
from scipy import stats

from .exceptions import IllegalArgumentError
from .utils import (all_are_integers_or_none, count_non_none, count_none,
                    gen_data_from_descriptive)


class StudentsIndT(object):

    @staticmethod
    def forward(x, y):
        """
        Calculate the T-test for the means of *two independent* samples of scores.

        This is a two-sided test for the null hypothesis that 2 independent samples
        have identical average (expected) values. This test assumes that the
        populations have identical variances by default.

        Parameters
        ----------
        a, b : array_like

        Returns
        -------
        statistic : float or array
            The calculated t-statistic.
        pvalue : float or array
            The two-tailed p-value.

        Notes
        -----
        We can use this test, if we observe two independent samples from
        the same or different population, e.g. exam scores of boys and
        girls or of two ethnic groups. The test measures whether the
        average (expected) value differs significantly across samples. If
        we observe a large p-value, for example larger than 0.05 or 0.1,
        then we cannot reject the null hypothesis of identical average scores.
        If the p-value is smaller than the threshold, e.g. 1%, 5% or 10%,
        then we reject the null hypothesis of equal averages.

        References
        ----------
        # Independent_two-sample_t-test
        .. [1] https://en.wikipedia.org/wiki/T-test

        .. [2] https://en.wikipedia.org/wiki/Welch%27s_t-test
        """
        t, p = stats.ttest_ind(x, y)
        mean = (np.mean(x), np.mean(y))
        std = (np.std(x, ddof=1), np.std(y, ddof=1))
        size = (len(x), len(y))
        std_pool = ((size[0]-1) * std[0] ** 2 + (size[1] - 1) * std[1] ** 2)
        d = (mean[0] - mean[1]) / sqrt(std_pool / (sum(size) - 2))

        return t, p, d

    # TODO: Add Docstring
    @staticmethod
    def inverse(p=.05, ef=.1, eq_size=False, size=None, mean=None, std=None,
                csize=[(5, 100), (5, 100)], cmean=[(-10, 10), (-10, 10)], cstd=[(.1, 5), (.1, 5)],
                tails=1, throw_err=True):
        # TODO: Initialize and check for valid arguments in 'csize', 'cmean', 'cstd'
        # TODO: Initialize and check for valid arguments in 'size', 'mean', 'std'
        if size is not None:
            if (len(size) == 2 and not all_are_integers_or_none(size)) or len(size) != 2:
                if throw_err:
                    raise IllegalArgumentError(
                        f"Expecting 'None' or list of integers and/or 'None' for 'size' argument. You provided {size}.")
                size = [None, None]
        else:
            size = [None, None]

        if mean is not None:
            if len(mean) != 2:
                if throw_err:
                    raise IllegalArgumentError(
                        f"Expecting 'None' or list of length 2 for 'mean' argument. You provided {mean}.")
                mean = [None, None]
        else:
            mean = [None, None]

        if std is not None:
            if len(std) != 2:
                if throw_err:
                    raise IllegalArgumentError(
                        f"Expecting 'None' or list of length 2 for 'std' argument. You provided {std}.")
                std = [None, None]
        else:
            std = [None, None]

        if tails not in [1, 2]:
            if throw_err:
                raise IllegalArgumentError(
                    f"Expecting either one or two tails. You provided {tails}.")
            else:
                tails = 1

        size, mean, std = StudentsIndT._inverse(
            p, ef, eq_size, size, mean, std, csize, cmean, cstd, tails, throw_err)

        data = gen_data_from_descriptive(mean, std, size)

        return size, mean, std, data

    @staticmethod
    def _inverse(p, ef, eq_size, size, mean, std, csize, cmean, cstd, tails, throw_err):

        size = StudentsIndT._find_size(
            p, ef, eq_size, size, csize, tails, throw_err)
        t = stats.t.ppf(1 - (p / tails), sum(size) - 2)
        ef_corr = abs(t * sqrt(1 / size[0] + 1 / size[1]))
        mean, std = StudentsIndT._find_mean_std(
            ef_corr, size, mean, std, cmean, cstd, tails, throw_err)

        return size, mean, std

    # TODO: Refactor to implement multiprocessing
    @staticmethod
    def _find_size(p, ef, eq_size, size, csize, tails, throw_err):
        size_comb = [size]

        # Single user sample size provided:
        if count_none(size) == 1:
            idx_prov_n, prov_n = (
                [(i, x) for i, x in enumerate(size) if x is not None])[0]
            ns_comb = [[prov_n, prov_n]]
            if not eq_size:
                ns_comb = product([prov_n], range(csize[1][0], csize[1][1]))
                if idx_prov_n == 1:
                    ns_comb = product(
                        range(csize[0][0], csize[0][1]), [prov_n])

        # No user sample sizes provided
        if count_none(size) == 2:
            ns_comb = [[x, x] for x in range(csize[0][0], csize[0][1] + 1)]
            if not eq_size:
                ns_comb = product(
                    range(csize[0][0], csize[0][1] + 1), range(csize[1][0], csize[1][1]))

        # Minimize distance between t-value produced from inverse t-dist using p-value,
        # and t-value produced from the Cohen's d effect size eq.
        min_diff = float("inf")
        ns_prime = None
        for i in ns_comb:
            t_from_p = stats.t.ppf(1 - (p / tails), sum(i) - 2)
            t_from_d = ef / sqrt(1 / i[0] + 1 / i[1])
            cur_diff = abs(abs(t_from_p) - abs(t_from_d))
            if cur_diff < min_diff:
                min_diff = cur_diff
                ns_prime = i

        if (count_none(size) == 1 or count_none(size) == 1) and not isclose(min_diff, 0, rel_tol=1):
            if throw_err:
                raise ValueError("Provided sample size/s will not produce desired inference statistics. "
                                 "Pick different sample size/s or remove it/them altogether.")

        return list(ns_prime)

    # TODO: Refactor to include bound checks for the variables
    @staticmethod
    def _find_mean_std(ef, size, mean, std, cmean, cstd, tails, throw_err, f_alpha=.05):
        # F-test for homogeneity of variances
        lb_f = stats.f.ppf(f_alpha / tails, size[0] - 1, size[1] - 1)
        ub_f = stats.f.ppf(1 - f_alpha / tails, size[0] - 1, size[1] - 1)

        # Both means and both standard deviations provided
        if count_non_none(mean) == 2 and count_non_none(std) == 2:
            if not lb_f < (std[0] / std[1]) ** 2 < ub_f:
                if throw_err:
                    raise ValueError("Provided standard deviations are not equal. Either try Welch's t-test "
                                     "or correct your standard deviations.")
            sd_p = sqrt(((size[0] - 1) * std[0] ** 2 + (size[1] - 1)
                         * std[1] ** 2) / (size[0] + size[1] - 2))
            mean_diff = mean[0] - mean[1]
            if not isclose(ef, mean_diff / sd_p, abs_tol=0.01):
                if throw_err:
                    raise ValueError("Provided means and standard deviations will not produce desired inference "
                                     "statistics. Pick different means and/or standard deviations or remove "
                                     "them altogether.")
                else:
                    mean = [None, None]
                    std = [None, None]

        #  Both means provided
        if count_non_none(mean) == 2:
            mean_diff = mean[0] - mean[1]
            sd_p = mean_diff / ef
            if count_non_none(std) == 1:
                prov_sd_idx, prov_sd = (
                    [(i, x) for i, x in enumerate(std) if x is not None])[0]
                std[1 - prov_sd_idx] = sqrt(
                    (sd_p * (size[0] + size[1] - 2) - (size[1 - prov_sd_idx] - 1) * prov_sd ** 2) / (size[prov_sd_idx] - 1))
            else:
                std[0] = (sd_p / 2) * np.random.uniform(1, 1.05)
                std[1] = sqrt((sd_p * (size[0] + size[1] - 2) -
                               (size[0] - 1) * std[0] ** 2) / (size[1] - 1))
            return mean, std

        # Both standard deviations are provided
        if count_none(std) == 0:
            if not lb_f < (std[0] / std[1]) ** 2 < ub_f:
                if throw_err:
                    raise ValueError("Provided standard deviations are not equal. Either try Welch's t-test "
                                     "or correct your standard deviations.")
                else:
                    std = [None, None]

        # Single standard deviation provided
        if count_none(std) == 1:
            prov_sd_idx, prov_sd = (
                [(i, x) for i, x in enumerate(std) if x is not None])[0]
            if prov_sd_idx == 0:
                cstd[1] = [max(std[0] / sqrt(ub_f), cstd[1][0]),
                           min(std[0] / sqrt(lb_f), cstd[1][1])]
            else:
                cstd[0] = [max(sqrt(lb_f) * std[1], cstd[0][0]),
                           min(sqrt(ub_f) * std[1], cstd[0][1])]
            std[1 - prov_sd_idx] = np.random.uniform(cstd[0][0], cstd[0][1]) if prov_sd_idx == 1 else uniform(cstd[1][0],
                                                                                                              cstd[1][1])
        # No standard deviation provided
        else:
            std[0] = np.random.uniform(cstd[0][0], cstd[0][1])
            cstd[1] = [max(std[0] / sqrt(ub_f), cstd[1][0]),
                       min(std[0] / sqrt(lb_f), cstd[1][1])]
            std[1] = np.random.uniform(cstd[1][0], cstd[1][1])

        sd_p = sqrt(((size[0] - 1) * std[0] ** 2 + (size[1] - 1)
                     * std[1] ** 2) / (size[0] + size[1] - 2))
        mean_diff = ef * sd_p

        if count_none(mean) == 1:
            prov_mean_idx, prov_mean = (
                [(i, x) for i, x in enumerate(mean) if x is not None])[0]
            mean[1 - prov_mean_idx] = mean_diff + \
                prov_mean if prov_mean_idx == 1 else prov_mean - mean_diff

        if count_none(mean) == 2:
            mean[0] = np.random.uniform(cmean[0][0], cmean[1][0])
            mean[1] = mean[0] - mean_diff

        return mean, std


class RANOVA(object):

    @staticmethod
    def forward(data):
        # TODO: Update Docstring
        """Null Hypothesis Significance Test for the Repeated Measurements ANOVA.

        Arguments:
            data {2D Array} -- A nxm matrix whos rows represent measurements for each n participants across m levels

        Keyword Arguments:
            ef_sz {bool} -- Flag whether the effect size should be returned as well. (default: {False})

        Returns:
            [tuple] -- 2-tuple containning test statistics and p-value, if ef_sz is set to False. 3-tuple containing the effect size as the last argument if ef_sz is set to True.
        """
        n, k = data.shape
        SS_M = n * np.sum((np.mean(data, axis=0) -
                           np.mean(np.mean(data, axis=0))) ** 2)
        SS_R = RANOVA._obj_fun(data, np.std(data, axis=0, ddof=1),
                               np.std(data, axis=1, ddof=1))[1] - SS_M
        df_M = k - 1
        df_R = (k-1)*(n-1)
        F = (SS_M/df_M)/(SS_R/df_R)

        return F, 1-stats.f.cdf(F, df_M, df_R), SS_M/(SS_M+SS_R)

    @staticmethod
    def inverse(p=.05, ef=.1, grps=4, size=None, mean=None,
                std=None, csize=(5, 100), cmean=(-10, 10), cstd=(.1, 10),
                gmean=42, runs=100, cycles=100, throw_err=True):
        # TODO: Add Docstrings
        # TODO: Verify 'csize', 'cmean', 'cstd'
        # TODO: Verify 'size', 'mean', 'std'
        if size is not None:
            if (len(size) == grps and not all_are_integers_or_none(size)) or len(size) != 2:
                if throw_err:
                    raise IllegalArgumentError(
                        f"Expecting 'None' or list of integers and/or 'None' of length {grps} for 'size' argument. You provided {size}.")
                size = None
        else:
            size = None

        if mean is not None:
            if len(mean) != grps:
                if throw_err:
                    raise IllegalArgumentError(
                        f"Expecting 'None' or list of length {grps} for 'mean' argument. You provided {mean}.")
                mean = [None for _ in range(grps)]
        else:
            mean = [None for _ in range(grps)]

        if std is not None:
            if len(std) != grps:
                if throw_err:
                    raise IllegalArgumentError(
                        f"Expecting 'None' or list of length {grps} for 'std' argument. You provided {std}.")
                std = [None for _ in range(grps)]
        else:
            std = [None for _ in range(grps)]

        size = RANOVA._find_size(p, ef, grps, size, csize, throw_err)
        mean = RANOVA._find_mean(grps, mean, gmean, throw_err)
        std_participant = RANOVA._find_std_participant(
            p, grps, size, mean, gmean)
        std = RANOVA._find_std(grps, std, std_participant, throw_err)
        data = RANOVA._generate_data(p, grps, size, csize, mean, std, std_participant, runs, cycles)

        return size, mean, std, data

    @staticmethod
    def _find_size(p, ef, grps, size, csize, throw_err):
        # TODO: Refactor implementing multiprocessing
        df_M = grps - 1
        _n = None
        f_from_ef = abs(ef / (1 - ef))
        min_diff = float("inf")
        for i in range(csize[0], csize[1] + 1):
            df_R = (grps - 1) * (i - 1)
            f_from_p = stats.f.ppf(1 - p, df_M, df_R) / (i - 1)
            cur_min_diff = abs(f_from_p - f_from_ef)
            if cur_min_diff < min_diff:
                min_diff = cur_min_diff
                _n = i

        # TODO: Update Error Message
        if (size is not None and
            not isclose(_n, size, abs_tol=5) and
                not csize[0] <= _n <= csize[1]):
            if throw_err:
                raise ValueError(
                    "User provided sample size doesn't fit the inferential statistics.")

        return _n

    @staticmethod
    def _find_mean(grps, mean, gmean, throw_err):
        if count_none(mean) == 0:
            if np.mean(mean) != gmean and throw_err:
                # TODO: Update Error Message
                raise ValueError(
                    "User provided means don't fit the provided global mean. Either change the global mean or loosen the provided group means.")
            else:
                gmean = np.mean(mean)
                return np.asarray(mean)

        for i, m in enumerate(mean):
            if m is not None:
                continue
            rest = (grps * gmean -
                    np.sum([mean for mean in mean if mean is not None]))
            factor = rest / count_none(mean)

            if i == len(mean) - 1:
                mean[i] = factor
            else:
                mean[i] = np.random.uniform(.2, 1.9) * factor

        return np.asarray(mean, dtype="float64")

    @staticmethod
    def _find_std_participant(p, grps, size, mean, gmean):
        # Initialize
        stds = [None for _ in range(size)]

        # Pre-Computations
        f_prime = stats.f.ppf(1 - p, grps - 1,
                              (grps - 1) * (size - 1)) / (size - 1)
        ss_M = size * (np.sum(np.power(mean, 2)) - gmean ** 2 * grps)
        ss_W = ss_M * (1 / f_prime + 1)

        # Computation
        for i, _ in enumerate(stds):
            factor = (ss_W / (grps - 1) -
                      np.sum([std_p for std_p in stds if std_p is not None])) / count_none(stds)

            if i == len(stds) - 1:
                stds[i] = factor
            else:
                stds[i] = np.random.uniform(.5, 1.5) * factor

        return np.sqrt(np.asarray(stds))

    @staticmethod
    def _find_std(grps, std, std_participant, throw_err):
        if count_none(std) == 0 and not np.isclose(np.mean(std), np.mean(std_participant), rtol=1.e-3):
            if throw_err:
                # TODO: Update Error Message
                raise ValueError(
                    f"User provided standard deviations of the levels are too different from the \
                    standard deviations of the participants. Either loosen the provided standard \
                    deviations or get the mean of the provided standard deviations closer to \
                    {np.mean(std_participant)}")
            else:
                std[np.random.randint(0, std.size)] = None

        while np.mean(std_participant) * grps < np.sum([x for x in std if not (x is None or np.isnan(x))]):
            if throw_err:
                # TODO: Update Error Message
                raise ValueError(f"User provided standard deviations of the levels are too different from the \
                    standard deviations of the participants. Either loosen the provided standard \
                    deviations or get the mean of the provided standard deviations closer to \
                    {np.mean(std_participant)}")
            std[np.random.randint(0, std.size)] = None

        for i, s in enumerate(std):
            if not (s is None or np.isnan(s)):
                continue
            rest = grps * np.mean(std_participant) - np.sum(
                [x for x in std if not (x is None or np.isnan(x))])
            factor = rest / count_none(std)

            if i == len(std) - 1:
                std[i] = factor
            else:
                std[i] = np.random.uniform(.9, 1.1) * factor

        return std

    @staticmethod
    def _obj_fun(data, stds_level, stds_participant):
        target_SS_W = np.sum(stds_participant ** 2) * (len(stds_level) - 1)
        data_col_stds = np.std(data, axis=1, ddof=1)
        data_SS_W = np.sum(data_col_stds ** 2) * (len(stds_level) - 1)
        return (data_SS_W - target_SS_W)**2, target_SS_W, data_SS_W

    @staticmethod
    def _generate_data(p, grps, size, csize, mean, std, std_participant, runs, cycles):
        combs = product([p], [grps], [size], [csize], [mean], [std], [
                        std_participant], [runs], range(cycles))

        with mp.Pool(processes=5) as pool:
            results = pool.starmap(RANOVA._optimized_insert_solver, combs)

        # Uncomment if you want to debug the '_optimized_insert_solver'
        # for i in combs:
        #     res = self._optimized_insert_solver_v2(*i)

        v = min(results, key=lambda t: t[1])

        return v[0]

    @staticmethod
    def _optimized_insert_solver(p, grps, size, csize, mean, std, std_participant, runs, cycle):
        data = np.empty((size, grps))
        RANOVA._init_result_matrix(data, mean, std)

        def _std_spec_mean(data, mean, df):
            return np.sqrt((np.sum((data - mean) ** 2)) / df)

        wc = np.copy(data)
        for i in range(runs):
            delta = np.std(wc, axis=1, ddof=1) - std_participant
            ind = np.argpartition(
                delta, -csize[0])[-csize[0]:]
            factor = _std_spec_mean(np.delete(
                wc[:, i % mean.size], ind), mean[i % mean.size], wc[:, i % mean.size].size - ind.size - 1)
            new_values = gen_data_from_descriptive(
                [mean[i % mean.size]], [factor], [ind.size])
            np.put(wc[:, i % grps], ind, new_values)
            if RANOVA._obj_fun(wc, std, std_participant)[0] < RANOVA._obj_fun(data, std, std_participant)[0]:
                data = wc

        return data, abs(p - RANOVA.forward(data)[1])/p

    @staticmethod
    def _init_result_matrix(data, means, stds):
        n, _ = data.shape
        for i, p in enumerate(zip(means, stds)):
            data[:, i] = gen_data_from_descriptive([p[0]], [p[1]], [n])[0]
