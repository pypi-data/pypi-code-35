# -*- coding: utf-8 -*-

"""
cheno.utils
~~~~~~~~~~~~~~
This module provides utility functions that are used within cheno
that are also useful for external consumption.
"""
import numpy as np

from math import sqrt

from .exceptions import IllegalArgumentError


NONPARAM_SUPPORTED_DIST = ['uniform']


def all_are_integers_or_none(xs):
    """ Return True if all the values are integers."""
    return all(type(x) is int for x in xs if not (x is None or np.isnan(x)))


def count_none(xs):
    """ Count number of 'None' or 'numpy.Nan' instances. """
    return len([1 for x in xs if x is None or np.isnan(x)])


def count_non_none(a):
    """ Count number of non 'None' or 'numpy.Nan' instances. """
    return len([1 for x in a if not (x is None or np.isnan(x))])


# TODO: Add Docstring
def gen_data_from_descriptive(means, stds, ns):
    if len(means) != len(stds) or len(stds) != len(ns):
        raise ValueError(f'Unequal size of parameters.')
    datasets = []
    for m, s, n in zip(means, stds, ns):
        s = sqrt(s ** 2 * ((n - 1) / n))
        datasets.append(_adjust(np.random.normal(m, s, n), m, s))
    return datasets


# TODO: Add Docstring
def gen_data_from_ranks(ranks, size_total, low=-5, high=5, dist='uniform'):
    if sum([len(x) for x in ranks]) != size_total:
        raise IllegalArgumentError(
            f"Number of ranks has to match with 'size_total'. {sum([len(x) for x in ranks])} != {size_total}")

    if dist not in NONPARAM_SUPPORTED_DIST:
        raise IllegalArgumentError(
            f"Distribution expected to match a supported distribution. You provided: {dist}")

    data = (np.random.uniform(low, high, size_total))
    data.sort()

    res = []
    for idx in ranks:
        res.append([data[i - 1] for i in idx])

    return res


def _adjust(data, mean, sd):
    return _adj_mean(_adj_std(data, target=sd), target=mean)


def _adj_mean(data, target=None, inc=None):
    y = data.mean()
    d = 0
    if target is not None:
        d = y - target
    elif inc is not None:
        d = inc
    else:
        raise ValueError('No manipulation strategy chosen.')
    return data - d


def _adj_std(data, target=None, inc=None):
    y = data.std()
    d = 1
    if target is not None:
        d = target / y
    elif inc is not None:
        d = inc
    else:
        raise ValueError('No manipulation strategy chosen.')
    return data * d
