#!/usr/bin/env python
#
# test_processing.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import itertools as it
import multiprocessing as mp
import string
import random

from unittest import mock

import numpy  as np
import pandas as pd
import           pytest

import ukbparse.processing           as processing
import ukbparse.importing            as importing
import ukbparse.custom               as custom
import ukbparse.processing_functions as pfns


from . import (gen_DataTable,
               clear_plugins,
               tempdir,
               gen_tables,
               gen_DataTableFromDataFrame)


def test_removeIfSparse():

    sparse = np.random.random(100)
    good   = np.random.random(100)

    sparse[:50] = np.nan

    dtable = gen_DataTable([good, sparse])
    remove = pfns.removeIfSparse(dtable, [1, 2], minpres=60)
    remove = [r.name for r in remove]
    assert remove == ['2-0.0']

    dtable = gen_DataTable([good, sparse])
    remove = pfns.removeIfSparse(dtable, [1, 2], minpres=40)
    remove = [r.name for r in remove]
    assert remove == []


def test_removeIfRedundant():

    series1 = np.sin(np.linspace(0, np.pi * 6, 100))
    series2 = series1 + np.random.random(100)
    corr    = pd.Series(series1).corr(pd.Series(series2))

    dtable = gen_DataTable([series1, series2])
    remove = pfns.removeIfRedundant(dtable, [1, 2], corr * 0.9)
    remove = [r.name for r in remove]

    assert remove == ['2-0.0']

    dtable = gen_DataTable([series1, series2])
    remove = pfns.removeIfRedundant(dtable, [1, 2], corr * 1.1)
    remove = [r.name for r in remove]

    assert remove == []


def  test_processData():           _test_processData(False)
def  test_processData_lowMemory(): _test_processData(True)
def _test_processData(lowMemory):

    custom.registerBuiltIns()

    sparse      = np.random.random(100)
    sparse[:50] = np.nan
    series1     = np.sin(np.linspace(0, np.pi * 6, 100))
    series2     = series1 + np.random.random(100)
    corr        = pd.Series(series1).corr(pd.Series(series2))

    vartable, proctable, cattable = gen_tables(range(1, 4))[:3]

    procs = [
        'removeIfSparse(60)',
        'removeIfRedundant({:0.2f})'.format(corr - 0.01)]

    procs  = [processing.parseProcesses(p, 'processor') for p in procs]
    procs  = [{p[0].name : p[0]} for p in procs]

    with tempdir(), mp.Pool(mp.cpu_count()) as pool:

        mgr = mp.Manager()

        df = pd.DataFrame({'1-0.0' : sparse,
                           '2-0.0' : series1,
                           '3-0.0' : series2},
                          index=np.arange(1, 101))
        df.index.name = 'eid'
        df.to_csv('data.txt')

        dtable, _ = importing.importData('data.txt',
                                         vartable,
                                         proctable,
                                         cattable,
                                         lowMemory=lowMemory,
                                         pool=pool,
                                         mgr=mgr)

        dtable.proctable['Variable'] = ['all_independent', 'all']
        dtable.proctable['Process']  = procs
        processing.processData(dtable)
        assert [c.name for c in dtable.allColumns[1:]] == ['2-0.0']

        dtable, _ = importing.importData('data.txt',
                                         vartable,
                                         proctable,
                                         cattable,
                                         lowMemory=lowMemory,
                                         pool=pool,
                                         mgr=mgr)
        dtable.proctable['Variable'] = [[2, 3], [1, 2]]
        dtable.proctable['Process']  = procs
        processing.processData(dtable)
        assert [c.name for c in dtable.allColumns[1:]] == \
            ['1-0.0', '2-0.0', '3-0.0']
        df = None
        mgr = None
        pool = None
        dtable = None


def test_parseProcesses_parser():

    parser = processing.makeParser()

    with mock.patch('ukbparse.custom.exists', return_value=True):

        p = processing.parseProcesses('blah', 'none')
        assert len(p)   == 1
        p = p[0]
        assert p.name   == 'blah'
        assert p.args   == ()
        assert p.kwargs == {}

        p = processing.parseProcesses('blah()', 'none')
        assert len(p)   == 1
        p = p[0]
        assert p.name   == 'blah'
        assert p.args   == ()
        assert p.kwargs == {}

        p = processing.parseProcesses('blah(1, 2)', 'none')
        assert len(p)   == 1
        p = p[0]
        assert p.name   == 'blah'
        assert p.args   == (1, 2)
        assert p.kwargs == {}

        p = processing.parseProcesses('blah("a", \'b\', 3)', 'none')
        assert len(p)   == 1
        p = p[0]
        assert p.name   == 'blah'
        assert p.args   == ('a', 'b', 3)
        assert p.kwargs == {}

        p = processing.parseProcesses('blah(a=1, b=2, c=3)', 'none')
        assert len(p)   == 1
        p = p[0]
        assert p.name   == 'blah'
        assert p.args   == ()
        assert p.kwargs == {'a' : 1, 'b' : 2, 'c' : 3}

        p = processing.parseProcesses('blah("a", b=2, c=3)', 'none')
        assert len(p)   == 1
        p = p[0]
        assert p.name   == 'blah'
        assert p.args   == ('a',)
        assert p.kwargs == {'b' : 2, 'c' : 3}


@clear_plugins
def test_parseProcesses_run():

    called = {}

    @custom.processor('boo')
    def boo(a, b):
        assert a == 1 and b == 'hah'
        called['boo'] = True

    @custom.processor('foo')
    def foo(c, d):
        assert c == 'wah' and d == 4
        called['foo'] = True

    @custom.cleaner('moo')
    def moo(*a):
        called['moo'] = True

    @custom.cleaner('woo')
    def woo(x, y):
        assert x == 10 and y == 20
        called['woo'] = True

    @custom.processor('hoo')
    def hoo(truearg, falsearg, nonearg):
        assert truearg is True
        assert falsearg is False
        assert nonearg is None
        called['hoo'] = True

    procs  = processing.parseProcesses(
        'boo(1, \'hah\'), foo("wah", 4), hoo(True, False, None)',
        'processor')
    pprocs = processing.parseProcesses(
        'moo, moo(), woo(10, 20)',
        'cleaner')

    assert procs[0].name == 'boo'
    assert procs[0].args == (1, 'hah')
    assert procs[1].name == 'foo'
    assert procs[1].args == ('wah', 4)
    assert procs[2].name == 'hoo'
    assert procs[2].args == (True, False, None)

    procs[0].run()
    procs[1].run()
    procs[2].run()

    assert called['boo']
    assert called['foo']
    assert called['hoo']

    assert pprocs[0].name == 'moo'
    assert pprocs[1].name == 'moo'
    assert pprocs[2].name == 'woo'
    assert pprocs[0].args == ()
    assert pprocs[1].args == ()
    assert pprocs[2].args == (10, 20)

    pprocs[0].run()
    assert called['moo']
    called.clear()
    pprocs[1].run()
    assert called['moo']
    pprocs[2].run()
    assert called['woo']

    with pytest.raises(processing.NoSuchProcessError):
        processing.parseProcesses('gurh', 'processor')
    with pytest.raises(processing.NoSuchProcessError):
        processing.parseProcesses('boo', 'cleaner')
    with pytest.raises(processing.NoSuchProcessError):
        processing.parseProcesses('moo', 'processor')


def test_binariseCateorical():

    data = np.random.randint(1, 10, (50, 14))
    data[:, 0] = np.arange(1, 51)
    cols = ['eid',
            '1-0.0', '1-1.0',
            '2-0.0', '2-1.0', '2-2.0',
            '3-0.0',
            '4-0.0', '4-0.1', '4-0.2',
            '5-0.0', '5-0.1', '5-1.0', '5-1.1']

    vids  = list(range(1, 6))
    didxs = list(range(1, 14))

    with tempdir():
        np.savetxt('data.txt', data, delimiter=',', header=','.join(cols))
        vartable, proctable, cattable = gen_tables(range(1, 13))[:3]
        dt, _ = importing.importData('data.txt', vartable, proctable, cattable)

        remove, add, addvids = pfns.binariseCategorical(
            dt, vids,
            acrossVisits=False,
            acrossInstances=False,
            nameFormat='{vid}-{visit}.{instance}.{value}')

        names = [cols[i] for i in didxs]
        assert [r.name for r in remove] == names

        uniqs = [(i, np.unique(data[:, i])) for i in didxs]
        offset = 0

        for didx, duniqs in uniqs:

            for u in duniqs:

                exp = data[:, didx] == u
                i = offset
                offset += 1

                assert addvids[i] == int(cols[didx].split('-')[0])
                assert add[i].name == '{}.{}'.format(cols[didx], int(u))
                assert (add[i] == exp).all()

        remove, add, addvids = pfns.binariseCategorical(
            dt, vids,
            acrossVisits=True,
            acrossInstances=False,
            nameFormat='{vid}.{instance}.{value}')

        names = []
        offset = 0
        for vid in vids:
            for instance in dt.instances(vid):
                cols = [c.name for c in dt.columns(vid, instance=instance)]
                uniqs = sorted(np.unique(dt[:, cols]))
                names.extend(cols)

                for u in uniqs:
                    exp = np.any(dt[:, cols] == u, axis=1)

                    i = offset
                    offset += 1
                    got = add[i]
                    assert addvids[i] == vid
                    assert got.name == '{}.{}.{}'.format(vid, instance, int(u))
                    assert (got == exp).all()
        assert names == [r.name for r in remove]

        remove, add, addvids = pfns.binariseCategorical(
            dt, vids,
            acrossVisits=False,
            acrossInstances=True,
            nameFormat='{vid}.{visit}.{value}')

        names = []
        offset = 0
        for vid in vids:
            for visit in dt.visits(vid):
                cols = [c.name for c in dt.columns(vid, visit=visit)]
                uniqs = sorted(np.unique(dt[:, cols]))
                names.extend(cols)

                for u in uniqs:
                    exp = np.any(dt[:, cols] == u, axis=1)

                    i = offset
                    offset += 1
                    got = add[i]
                    assert addvids[i] == vid
                    assert got.name == '{}.{}.{}'.format(vid, visit, int(u))
                    assert (got == exp).all()
        assert names == [r.name for r in remove]

        remove, add, addvids = pfns.binariseCategorical(
            dt, vids,
            acrossVisits=True,
            acrossInstances=True,
            nameFormat='{vid}.{value}')

        names = []
        offset = 0
        for vid in vids:
            cols = [c.name for c in dt.columns(vid)]
            uniqs = sorted(np.unique(dt[:, cols]))
            names.extend(cols)

            for u in uniqs:
                exp = np.any(dt[:, cols] == u, axis=1)

                i = offset
                offset += 1
                got = add[i]
                assert addvids[i] == vid
                assert got.name == '{}.{}'.format(vid, int(u))
                assert (got == exp).all()
        assert names == [r.name for r in remove]


def test_binariseCategorical_nonnumeric():

    data = [random.choice(string.ascii_letters[:8]) for i in range(40)]
    data = [data[:20], data[20:]]

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write('eid, 1-0.0, 1-1.0\n')
            for i, (v1, v2) in enumerate(zip(*data)):
                f.write('{}, {}, {}\n'.format(i + 1, v1, v2))

        vartable, proctable, cattable = gen_tables([1])[:3]
        dt, _ = importing.importData('data.txt', vartable, proctable, cattable)

        remove, add, addvids = pfns.binariseCategorical(
            dt, [1],
            acrossVisits=True,
            acrossInstances=True,
            nameFormat='{vid}.{value}')

        unique   = set(data[0] + data[1])
        remnames = [r.name for r in remove]
        addnames = [a.name for a in add]

        assert '1-0.0' in remnames and '1-1.0' in remnames
        assert len(addvids) == len(add)
        assert all([v == 1 for v in addvids])

        for u in unique:
            name = '1.{}'.format(u)
            assert name in addnames

            series = add[addnames.index(name)]
            mask = [u == data[0][i] or u == data[1][i] for i in range(20)]

            assert (series == mask).all()


def test_expandCompound():

    data = []

    for i in range(20):
        rlen = np.random.randint(1, 20)
        row = np.random.randint(1, 100, rlen)
        data.append(row)

    exp = np.full((len(data), max(map(len, data))), np.nan)

    for i in range(len(data)):
        exp[i, :len(data[i])] = data[i]

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write('eid\t1-0.0\n')
            for i in range(len(data)):
                f.write(str(i + 1) + '\t' + ','.join(map(str, data[i])))
                f.write('\n')

        vartable, proctable, cattable = gen_tables([1])[:3]
        dt, _ = importing.importData('data.txt', vartable, proctable, cattable)

        dt[:, '1-0.0'] = dt[:, '1-0.0'].apply(
            lambda v: np.fromstring(v, sep=','))

        remove, add, addvids = pfns.expandCompound(dt, [1])

        assert [r.name for r in remove] == ['1-0.0']
        assert len(add) == max(map(len, data))
        assert len(addvids) == len(add)
        assert all([v == 1 for v in addvids])

        for col in range(exp.shape[1]):
            expcol = exp[:, col]
            gotcol = add[col].values

            expna = np.isnan(expcol)
            gotna = np.isnan(gotcol)

            assert np.all(        expna  ==         gotna)
            assert np.all(expcol[~expna] == gotcol[~gotna])
