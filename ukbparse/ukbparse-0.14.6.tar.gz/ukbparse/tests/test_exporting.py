#!/usr/bin/env python
#
# test_exporting.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import warnings
import textwrap as tw

import pandas as pd
import numpy  as np
import           h5py

import ukbparse.importing      as importing
import ukbparse.exporting      as exporting
import ukbparse.exporting_hdf5 as exporting_hdf5
import ukbparse.datatable      as datatable
import ukbparse.custom         as custom
import ukbparse.util           as util

from . import (gen_DataTable,
               clear_plugins,
               tempdir,
               gen_test_data,
               gen_tables,
               gen_DataTableFromDataFrame)


def test_genColumnNames():

    testdata = np.random.randint(1, 10, (10, 10))
    dtable   = gen_DataTable(testdata)

    dtable.vartable.loc[6, 'Description'] = 'abcde'

    colpat = '{variable}|{name}|{description}|{visit}|{instance}'
    colmap = { '1-0.0' : 'variable_one', '2-0.0' : 'variable_two'}
    names  = exporting.genColumnNames(dtable, colpat, colmap)

    exp = ['variable_one',
           'variable_two',
           '3|3-0.0||0|0',
           '4|4-0.0||0|0',
           '5|5-0.0||0|0',
           '6|6-0.0|abcde|0|0',
           '7|7-0.0||0|0',
           '8|8-0.0||0|0',
           '9|9-0.0||0|0',
           '10|10-0.0||0|0']

    exp = {c.name : n for c, n in zip(dtable.allColumns[1:], exp)}

    assert exp == names


def test_exportData():

    custom.registerBuiltIns()

    testdata = np.random.randint(1, 10, (10, 10)).astype(np.float32)

    def check(gotfile, expected):
        with open(gotfile, 'rt') as f:
            got = f.read().strip()
            return got == expected

    with tempdir():

        dtable = gen_DataTable(testdata)
        exporting.exportData(dtable, 'data.tsv', colpat='{variable}')
        exp = ['\t'.join(['eid'] +
                         ['{}'.format(i) for i in range(1, 11)])] + \
              ['\t'.join([str(i + 1)] + [str(c) for c in r])
               for i, r in enumerate(testdata.T)]
        exp = '\n'.join(exp)
        assert check('data.tsv', exp)

        td = np.copy(testdata)
        td[5, 5] = np.nan
        dtable = gen_DataTable(td)
        exporting.exportData(dtable,
                             'data.tsv',
                             colpat='{variable}',
                             colmap={'1-0.0' : 'var1'},
                             idcol='sub',
                             sep='*',
                             missingValues='boo')
        exp = ['*'.join(['sub', 'var1'] +
                         ['{}'.format(i)  for i in range(2, 11)])] + \
              ['*'.join([str(i + 1)] +
                        ['boo' if np.isnan(c) else str(c) for c in r])
               for i, r in enumerate(td.T)]
        exp = '\n'.join(exp)
        assert check('data.tsv', exp)



def test_exportData_subjid():

    custom.registerBuiltIns()

    with tempdir():
        gen_test_data(3, 3, 'data.tsv', start_subj=10)

        variables = list(range(0, 4))
        vartable, proctable, cattable, _ = gen_tables(variables)
        colnames  = ['eid'] + ['{}-0.0'.format(v) for v in variables[1:]]
        colobjs   = [datatable.Column(None, c, i, v, 0, 0)
                     for i, (c, v) in enumerate(zip(colnames, variables))]
        data      = pd.read_csv( 'data.tsv', delimiter='\t', index_col=0)

        dtable = datatable.DataTable(
            data, colobjs, vartable, proctable, cattable)

        exporting.exportData(dtable, 'export.tsv')

        got = pd.read_csv('export.tsv', delimiter='\t', index_col=0)

        assert np.all(got.index == [10, 11, 12])


@clear_plugins
def test_exportData_varformats():

    custom.registerBuiltIns()

    def check(gotfile, expected):
        with open(gotfile, 'rt') as f:
            got = f.read().strip()
            return got == expected

    datefmt  = '%Y a %m b %d c'
    timefmt  = '%Y a %m b %d c %M d %H e %S'
    floatfmt = '{} poo'

    @custom.formatter('test_datefmt')
    def datefmt_func(dtable, column, series):
        def format(val):
            return val.strftime(datefmt)
        return series.apply(format)


    @custom.formatter('test_timefmt')
    def timefmt_func(dtable, column, series):
        def format(val):
            return val.strftime(timefmt)
        return series.apply(format)


    @custom.formatter('test_floatfmt')
    def floatfmt_func(dtable, column, series):
        def format(val):
            return floatfmt.format(val)
        return series.apply(format)


    with tempdir():

        gen_test_data(
            3, 3, 'data.tsv', ctypes={1 : 'date', 2 : 'datetime'})

        variables = list(range(1, 4))

        vartable, proctable, cattable, _ = gen_tables(
            variables, {1 : 'Date', 2 : 'Time'})
        colnames  = ['{}-0.0'.format(v) for v in variables]
        colobjs   = [datatable.Column(None, 'eid', 0, 0, 0, 0)] + \
                    [datatable.Column(None, c, i, v, 0, 0)
                     for i, (c, v) in enumerate(zip(colnames, variables), 1)]

        data   = pd.read_csv(
            'data.tsv', delimiter='\t',
            parse_dates=['1-0.0', '2-0.0'],
            index_col=0,
            infer_datetime_format=True)

        dtable = datatable.DataTable(
            data, colobjs, vartable, proctable, cattable)

        expdates  = [v.strftime(datefmt) for v in data['1-0.0']]
        exptimes  = [v.strftime(timefmt) for v in data['2-0.0']]
        expfloats = [ floatfmt.format(v) for v in data['3-0.0']]

        exporting.exportData(dtable,
                             'export.tsv',
                             dateFormat='test_datefmt',
                             timeFormat='test_timefmt',
                             formatters={ 3 : 'test_floatfmt'})

        got = pd.read_csv('export.tsv', delimiter='\t', dtype=str, index_col=0)

        assert np.all(got['1-0.0'] == expdates)
        assert np.all(got['2-0.0'] == exptimes)
        assert np.all(got['3-0.0'] == expfloats)

        expdates = exporting.defaultDateTimeFormat(
            dtable, colobjs[1], dtable[:, '1-0.0'])
        exptimes = exporting.defaultDateTimeFormat(
            dtable, colobjs[2], dtable[:, '2-0.0'])

        exporting.exportData(dtable, 'export.tsv')

        got = pd.read_csv('export.tsv', delimiter='\t', dtype=str, index_col=0)

        assert np.all(got['1-0.0'] == expdates)
        assert np.all(got['2-0.0'] == exptimes)


def test_exportData_TSV_subject_ordering():

    custom.registerBuiltIns()

    with tempdir():
        data   = np.random.randint(1, 10, (5, 20))
        dtable = gen_DataTable(data)

        exporting.exportData(dtable, 'data.tsv', subjects=[10, 8, 6, 4, 2])
        got = pd.read_csv('data.tsv', delimiter='\t', index_col=0)
        assert np.all(got.index == [10, 8, 6, 4, 2])

        exporting.exportData(dtable,
                             'data.tsv',
                             subjects=[10, 8, 6, 4, 2],
                             numRows=2)
        got = pd.read_csv('data.tsv', delimiter='\t', index_col=0)
        assert np.all(got.index == [10, 8, 6, 4, 2])


def test_exportData_numRows():

    custom.registerBuiltIns()

    with tempdir():
        data   = np.random.randint(1, 10, (5, 20))
        dtable = gen_DataTable(data)

        exporting.exportData(dtable, 'nochunks.tsv')
        exporting.exportData(dtable, 'chunks.tsv', numRows=2)

        with open('nochunks.tsv', 'rt') as f: nochunks = f.read()
        with open('chunks.tsv',   'rt') as f: chunks   = f.read()

        assert nochunks == chunks


def test_defaultDateTimeFormat():

    custom.registerBuiltIns()

    with tempdir():
        gen_test_data(3, 3, 'data.tsv', ctypes={1 : 'date', 2 : 'datetime'})

        data = pd.read_csv('data.tsv',
                           delimiter='\t',
                           parse_dates=['1-0.0', '2-0.0'],
                           infer_datetime_format=True,
                           index_col=0)
        dt = gen_DataTableFromDataFrame(data)

        dt.vartable.loc[1, 'Type'] = util.CTYPES.date
        dt.vartable.loc[2, 'Type'] = util.CTYPES.time

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            datecol        = dt[:, '1-0.0']
            datecol[2]     = np.nan
            dt[:, '1-0.0'] = datecol

        def datefmt(d):
            try:    return d.strftime('%Y-%m-%d')
            except: return np.nan
        def timefmt(t):
            try:    return t.strftime('%Y-%m-%dT%H:%M:%S%z')
            except: return np.nan

        expdate = data['1-0.0'].apply(datefmt)
        exptime = data['2-0.0'].apply(timefmt)
        expvar  = data['3-0.0']

        gotdate = exporting.defaultDateTimeFormat(
            dt, dt.columns(1)[0], data['1-0.0'])
        gottime = exporting.defaultDateTimeFormat(
            dt, dt.columns(2)[0], data['2-0.0'])
        gotvar  = exporting.defaultDateTimeFormat(
            dt, dt.columns(3)[0], data['3-0.0'])

        expdna = expdate.isna()
        exptna = exptime.isna()

        assert np.all(expdate.isna() == expdna)
        assert np.all(exptime.isna() == exptna)

        assert np.all(expdate[~expdna] == gotdate[~expdna])
        assert np.all(exptime[~exptna] == gottime[~exptna])
        assert np.all(expvar           == gotvar)


def test_exportHDF5():

    custom.registerBuiltIns()

    with tempdir():
        gen_test_data(5, 10, 'data.tsv', ctypes={1 : 'date', 2 : 'datetime'})

        colnames = ['one', 'two', 'three', 'four', 'five']

        data = pd.read_csv('data.tsv',
                           delimiter='\t',
                           parse_dates=['1-0.0', '2-0.0'],
                           infer_datetime_format=True,
                           index_col=0)
        dt = gen_DataTableFromDataFrame(data)

        exporting_hdf5.exportHDF5(dt,
                                  'out_ukbparse.h5',
                                  list(dt.index),
                                  'eid',
                                  colnames,
                                  key='h5key',
                                  style='ukbparse')
        exporting_hdf5.exportHDF5(dt,
                                  'out_pandas.h5',
                                  list(dt.index),
                                  'eid',
                                  colnames,
                                  key='h5key',
                                  style='pandas')

        exp    = dt[:, :]
        gotpd  = pd.read_hdf('out_pandas.h5')
        gotukb = h5py.File('out_ukbparse.h5', 'r')
        assert gotpd.index.name     == 'eid'
        assert np.all(gotpd.columns == colnames)

        for i, c in enumerate(exp.columns):
            assert np.all(gotpd[colnames[i]] == exp[c])

        gotidx = gotukb['h5key/eid']

        assert np.all(exp.index[:] == gotidx)

        for i, col in enumerate(dt.allColumns[1:]):
            coldata = gotukb['h5key/{}'.format(colnames[i])]

            if col.name in ('1-0.0', '2-0.0'):
                expcol = exporting.defaultDateTimeFormat(
                    dt, col, exp[col.name])
            else:
                expcol = exp[col.name]

            assert np.all(np.asarray(coldata) == expcol)


def test_exportData_HDF_subject_ordering():

    custom.registerBuiltIns()

    with tempdir():
        data   = np.random.randint(1, 10, (5, 20))
        dtable = gen_DataTable(data)

        # pandas style + no chunking
        exporting.exportData(dtable,
                             'data.h5',
                             fileFormat='hdf5',
                             subjects=[10, 8, 6, 4, 2])
        got  = pd.read_hdf('data.h5')
        assert np.all(got.index == [10, 8, 6, 4, 2])

        # pandas style + chunking
        exporting.exportData(dtable,
                             'data.h5',
                             fileFormat='hdf5',
                             subjects=[10, 8, 6, 4, 2],
                             numRows=2)
        got  = pd.read_hdf('data.h5')
        assert np.all(got.index == [10, 8, 6, 4, 2])

        # ukbparse style
        exporting.exportData(dtable,
                             'data.h5',
                             style='ukbparse',
                             fileFormat='hdf5',
                             subjects=[10, 8, 6, 4, 2])

        got = exporting_hdf5.importUKBParseStyle(
            'data.h5', 'eid', key='ukbparse')

        assert np.all(got.index == [10, 8, 6, 4, 2])



def test_compound():

    data = tw.dedent("""
    "eid","1-0.0","2-0.0"
    1,"1,2,3",8
    2,"4,5,6",8
    3,"7,8,9",8
    """).strip()

    exp = tw.dedent("""
    eid\t1-0.0\t2-0.0
    1\t1.0,2.0,3.0\t8
    2\t4.0,5.0,6.0\t8
    3\t7.0,8.0,9.0\t8
    """).strip()


    def parseCompound(v):
        return np.fromstring(v, sep=',')

    with tempdir():

        with open('data.txt', 'wt') as f:
            f.write(data)

        vartable, proctable, cattable, _ = gen_tables([1, 2])
        dt, _ = importing.importData('data.txt', vartable, proctable, cattable)

        dt[:, '1-0.0'] = dt[:, '1-0.0'].apply(parseCompound)

        exporting.exportData(dt,
                             'out.txt',
                             fileFormat='tsv',
                             formatters={1 : 'compound'})

        with open('out.txt', 'rt') as f:
            got = f.read().strip()

        assert got == exp


def test_exporting_id_column():
    data = tw.dedent("""
    my_id,col1
    1,11
    2,12
    3,13
    """).strip()

    custom.registerBuiltIns()

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write(data)

        vartable, proctable, cattable, _ = gen_tables([1])
        dt, _ = importing.importData('data.txt', vartable, proctable, cattable)

        exporting.exportData(dt,
                             'out.txt',
                             fileFormat='tsv')


        got = pd.read_csv('out.txt', delimiter='\t', index_col=0)
        assert got.index.name == 'my_id'

        exporting.exportData(dt,
                             'out.txt',
                             fileFormat='tsv',
                             idcol='my_id_renamed')
        got = pd.read_csv('out.txt', delimiter='\t', index_col=0)
        assert got.index.name == 'my_id_renamed'


def test_exporting_no_data():

    data = tw.dedent("""
    eid,1-0.0,2-0.0
    1,11,21
    2,12,22
    3,13,23
    4,14,24
    5,15,25
    """)

    custom.registerBuiltIns()

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write(data)

        vartable, proctable, cattable, _ = gen_tables([1])
        dt, _ = importing.importData(
            'data.txt', vartable, proctable, cattable, variables=[3])

        exporting.exportData(dt,
                             'out.txt',
                             fileFormat='tsv')

        exp = "eid\n1\n2\n3\n4\n5"
        got = open('out.txt').read().strip()
        assert exp == got
