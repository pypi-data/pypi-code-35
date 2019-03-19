#!/usr/bin/env python
#
# test_processing_core.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import itertools as it

import numpy  as np
import pandas as pd


import ukbparse.util                      as util
import ukbparse.processing_functions_core as core


def test_isSparse_minpres():

    size = 100
    actual_present    = [0,  0.01, 0.1, 0.5, 1]
    minpres_threshold = [0,  0.01, 0.1, 0.5, 1]

    for present, threshold in it.product(actual_present, minpres_threshold):

        data     = np.random.random(size)
        expected = present < threshold

        missing = int(round(size - present * size))
        missing = np.random.choice(range(size), missing, replace=False)
        data[missing] = np.nan

        data = pd.Series(data)

        abs_result  = core.isSparse(data, util.CTYPES.continuous,
                                    minpres=threshold * size)
        prop_result = core.isSparse(data, util.CTYPES.continuous,
                                    minpres=threshold,
                                    absolute=False)

        assert expected == abs_result
        assert expected == prop_result

    # minpres should be ignored if
    # number of points in data is
    # less than or equal to it
    data = np.random.random(10)
    data[:2] = np.nan
    assert     core.isSparse(pd.Series(data),
                             util.CTYPES.continuous,
                             minpres=9)
    assert     core.isSparse(pd.Series(data),
                             util.CTYPES.continuous,
                             minpres=10)
    assert not core.isSparse(pd.Series(data),
                             util.CTYPES.continuous,
                             minpres=11)
    assert not core.isSparse(pd.Series(data),
                             util.CTYPES.continuous,
                             minpres=100)



def test_isSparse_minstd():

    actualstds = np.linspace(0, 2, 10)
    minstds    = np.linspace(0, 2, 10)

    size = 500

    for actualstd, minstd in it.product(actualstds, minstds):

        data      = np.random.randn(size) * actualstd
        data      = pd.Series(data)
        actualstd = data.std()
        expected  = actualstd <= minstd

        result = core.isSparse(data, util.CTYPES.continuous,
                               minstd=minstd)
        assert expected == result


def test_isSparse_maxcat():

    size          = 20
    actualmaxcats = np.linspace(1.0 / size, 1, size)[::2]
    maxcats       = np.linspace(1.0 / size, 1, size)[::2]

    for actualmaxcat, maxcat in it.product(actualmaxcats, maxcats):

        iamc = int(round(actualmaxcat * size))
        data = np.arange(size)
        data[:iamc] = size + 1

        data = pd.Series(data)

        expected = actualmaxcat >= maxcat

        # test should only be applied for integer/categoricals
        assert not core.isSparse(data, util.CTYPES.continuous,
                                 maxcat=maxcat)

        result = core.isSparse(data, util.CTYPES.integer,
                                maxcat=maxcat)
        assert expected == result

        result = core.isSparse(data, util.CTYPES.categorical_single,
                               maxcat=maxcat)
        assert expected == result

        result = core.isSparse(data, util.CTYPES.categorical_multiple,
                               maxcat=maxcat)
        assert expected == result


def test_redundantColumns():

    size    = 50
    series1 = np.sin(np.linspace(0, np.pi * 6, size))
    series2 = series1 + np.random.random(size)
    corr = pd.Series(series1).corr(pd.Series(series2))

    data = pd.DataFrame({0 : pd.Series(series1), 1 : pd.Series(series2)})
    cols = [0, 1]

    assert core.redundantColumns(data, cols, corr * 1.01) == []
    assert core.redundantColumns(data, cols, corr * 0.99) == [1]

    # insert some missing values, making
    # sure there are more missing values
    # in series2, and the missingness will
    # be positively correlated
    s1miss = np.random.choice(
        np.arange(size, dtype=np.int), 10, replace=False)
    s2miss = list(s1miss)
    while len(s2miss) < 13:
        idx = np.random.randint(0, size, 1)
        if idx not in s1miss:
            s2miss.append(idx)
    s2miss = np.array(s2miss, dtype=np.int)

    series1[s1miss] = np.nan
    series2[s2miss] = np.nan

    corr   = pd.Series(series1).corr(pd.Series(series2))
    nacorr = np.corrcoef(np.isnan(series1), np.isnan(series2))[0, 1]

    data = pd.DataFrame({0 : pd.Series(series1), 1 : pd.Series(series2)})

    assert core.redundantColumns(data, cols, corr * 1.01) == []
    assert core.redundantColumns(data, cols, corr * 0.99) == [1]

    # both present and missing values must
    # be above the threshold for the column
    # to be considered redundant
    assert core.redundantColumns(data, cols, corr * 0.99, nacorr * 0.99) == [1]
    assert core.redundantColumns(data, cols, corr * 1.01, nacorr * 0.99) == []
    assert core.redundantColumns(data, cols, corr * 0.99, nacorr * 1.01) == []
    assert core.redundantColumns(data, cols, corr * 1.01, nacorr * 1.01) == []

    # the column with more missing values
    # should be the one flagged as redundant
    data = pd.DataFrame({0 : pd.Series(series2), 1 : pd.Series(series1)})
    assert core.redundantColumns(data, cols, corr * 1.01)                == []
    assert core.redundantColumns(data, cols, corr * 0.99)                == [0]
    assert core.redundantColumns(data, cols, corr * 0.99, nacorr * 0.99) == [0]
    assert core.redundantColumns(data, cols, corr * 1.01, nacorr * 0.99) == []
    assert core.redundantColumns(data, cols, corr * 0.99, nacorr * 1.01) == []
    assert core.redundantColumns(data, cols, corr * 1.01, nacorr * 1.01) == []


def test_binariseCategorical():

    data = np.random.randint(1, 10, (100, 10))
    cols = {str(i + 1) : data[:, i] for i in range(10)}
    df   = pd.DataFrame(cols)

    bindata, uniq = core.binariseCategorical(df)

    assert sorted(uniq) == sorted(np.unique(data))

    for i, v in enumerate(uniq):
        exp = np.any(data == v, axis=1)
        assert np.all(bindata[:, i] == exp)

    data[data == 5] = 6
    data[:10, 0] = 5
    cols = {str(i + 1) : data[:, i] for i in range(10)}
    df   = pd.DataFrame(cols)

    bindata, uniq = core.binariseCategorical(df, minpres=11)

    assert sorted(uniq) == [1, 2, 3, 4, 6, 7, 8, 9]

    for i, v in enumerate(uniq):
        exp = np.any(data == v, axis=1)
        assert np.all(bindata[:, i] == exp)


def test_binariseCategorical_missing():

    data = np.full((50, 5), np.nan)

    for i in range(data.shape[1]):
        namask = np.random.random(data.shape[0]) < 0.1
        data[~namask, i] = np.random.randint(1, 10, (~namask).sum())

    expuniq = list(sorted(np.unique(data[~np.isnan(data)])))

    expdata = np.zeros((data.shape[0], len(expuniq)))

    for i, v in enumerate(expuniq):
        expdata[:, i] = np.any(data == v, axis=1)

    cols = {str(i + 1) : data[:, i] for i in range(data.shape[1])}
    df   = pd.DataFrame(cols)

    gotdata, gotuniq = core.binariseCategorical(df)
    assert np.all(gotuniq == expuniq)
    assert np.all(gotdata == expdata)


def test_expandCompound():

    data = []

    for i in range(20):
        rlen = np.random.randint(1, 20)
        row = np.random.randint(1, 100, rlen)
        data.append(row)

    exp = np.full((20, max(map(len, data))), np.nan)

    for i in range(20):
        exp[i, :len(data[i])] = data[i]

    series = pd.Series(data)

    got = core.expandCompound(series)

    expna = np.isnan(exp)
    gotna = np.isnan(got)

    assert np.all(     expna  ==      gotna)
    assert np.all(exp[~expna] == got[~gotna])
