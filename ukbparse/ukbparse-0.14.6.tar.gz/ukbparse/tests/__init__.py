#!/usr/bin/env python
#
# __init__.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import itertools     as it
import functools     as ft
import unittest.mock as mock
import                  os
import                  shutil
import                  logging
import                  tempfile
import                  contextlib
import                  collections

import datetime

import numpy as np
import pandas as pd

import ukbparse.util       as util
import ukbparse.custom     as custom
import ukbparse.loadtables as loadtables
import ukbparse.datatable  as datatable


def patch_logging(func):

    log                   = mock.MagicMock()
    log.getEffectiveLevel = lambda : logging.INFO

    def wrapper(*a, **kwa):
        with mock.patch('ukbparse.cleaning.log',             log), \
             mock.patch('ukbparse.cleaning_functions.log',   log), \
             mock.patch('ukbparse.config.log',               log), \
             mock.patch('ukbparse.custom.log',               log), \
             mock.patch('ukbparse.datatable.log',            log), \
             mock.patch('ukbparse.exporting.log',            log), \
             mock.patch('ukbparse.exporting_hdf5.log',       log), \
             mock.patch('ukbparse.exporting_tsv.log',        log), \
             mock.patch('ukbparse.expression.log',           log), \
             mock.patch('ukbparse.fileinfo.log',             log), \
             mock.patch('ukbparse.importing.log',            log), \
             mock.patch('ukbparse.loadtables.log',           log), \
             mock.patch('ukbparse.main.log',                 log), \
             mock.patch('ukbparse.processing.log',           log), \
             mock.patch('ukbparse.processing_functions.log', log), \
             mock.patch('ukbparse.util.log'):
            return func(*a, **kwa)
    return ft.update_wrapper(wrapper, func)


def clear_plugins(func):
    def wrapper(*a, **kwa):
        result = func(*a, **kwa)
        custom.clearRegistry()
        return result

    return ft.update_wrapper(wrapper, func)


@contextlib.contextmanager
def tempdir(root=None, changeto=True):

    testdir = tempfile.mkdtemp(dir=root)
    prevdir = os.getcwd()
    try:

        if changeto:
            os.chdir(testdir)
        yield testdir

    finally:
        if changeto:
            os.chdir(prevdir)
        shutil.rmtree(testdir)


def gen_test_data(num_vars,
                  num_subjs,
                  out_file,
                  max_visits=1,
                  max_instances=1,
                  start_var=1,
                  start_subj=1,
                  sep='\t',
                  ctypes=None,
                  missprop=0,
                  names=None,
                  min_visits=1):

    if ctypes is None:
        ctypes = {}


    varids = []
    cols   = []

    for varid in range(start_var, num_vars + start_var):

        nvisits    = np.random.randint(min_visits, max_visits    + 1)
        ninstances = np.random.randint(1,          max_instances + 1)

        for visit, instance in it.product(range(nvisits), range(ninstances)):
            cols.append(util.generateColumnName(varid, visit, instance))
            varids.append(varid)

    # subject IDs
    data = pd.DataFrame(index=range(start_subj, num_subjs + start_subj))
    data.index.name = 'eid'

    for varid, col in zip(varids, cols):
        ctype = ctypes.get(varid, 'float')

        if ctype == 'int':
            coldata = np.random.randint(1, 100, num_subjs)
        elif ctype == 'float':
            coldata = np.random.randint(1, 100, num_subjs)
        elif ctype == 'date':
            ys = np.random.randint(2000, 2019, num_subjs)
            ms = np.random.randint(1,    13,   num_subjs)
            ds = np.random.randint(1,    28,   num_subjs)
            coldata = [datetime.date(y, m, d) for y, m, d in zip(ys, ms, ds)]
        elif ctype == 'time':
            hs = np.random.randint(0,    23, num_subjs)
            ms = np.random.randint(0,    59, num_subjs)
            ss = np.random.randint(0,    59, num_subjs)
            coldata = [datetime.time(h, m, s) for h, m, s in zip(hs, ms, ss)]
        elif ctype == 'datetime':
            ys  = np.random.randint(2000, 2019, num_subjs)
            mos = np.random.randint(1,    13,   num_subjs)
            ds  = np.random.randint(1,    28,   num_subjs)
            hs  = np.random.randint(0,    23,   num_subjs)
            mis = np.random.randint(0,    59,   num_subjs)
            ss  = np.random.randint(0,    59,   num_subjs)
            coldata = [datetime.datetime(y, mo, d, h, mi, s)
                       for y, mo, d, h, mi, s in zip(ys, mos, ds, hs, mis, ss)]

        data[col] = coldata

        if missprop > 0:
            missing = np.random.choice(data.index,
                                       int(round(missprop * num_subjs)))
            data.loc[missing, col] = np.nan

    if names is None:
        names = True
    data.to_csv(out_file, sep, header=names)


table_headers  = {

    'variables'   : 'ID\tType\tDescription\tDataCoding\tNAValues\tRawLevels\tNewLevels\tParentValues\tChildValues\tClean',  # noqa
    'datacodings' : 'ID\tNAValues\tRawLevels\tNewLevels',
    'categories'  : 'ID\tCategory\tVariables',
    'types'       : 'Type\tClean',
    'processing'  : 'Variable\Process'
}

table_templates = {
    'variables'   : '{variable}\t{type}\t\t\t\t\t\t\t\t',
    'datacodings' : '',
    'categories'  : '',
    'types'       : '',
    'processing'  : '',
}

def gen_tables(variables, vtypes=None):

    if vtypes is None:
        vtypes = {}

    with tempdir():

        with open('datafile.txt', 'wt') as f:
            colnames = ['eid'] + ['{}-0.0'.format(v) for v in variables]
            f.write('\t'.join(colnames))

        for table in ['variables',
                      'datacodings',
                      'categories',
                      'types',
                      'processing']:

            fname = '{}.tsv'.format(table)
            hdr   = table_headers[  table]
            tmpl  = table_templates[table]

            with open(fname, 'wt') as f:
                f.write(hdr + '\n')

                if table == 'variables':
                    for v in variables:

                        vtype = str(vtypes.get(v, ''))

                        f.write(tmpl.format(variable=v, type=vtype) + '\n')

        return loadtables.loadTables(
            ['datafile.txt'],
            'variables.tsv',
            'datacodings.tsv',
            'types.tsv',
            'processing.tsv',
            'categories.tsv')


def gen_DataTable(cols, *a, **kwa):

    nsubjs    = len(cols[0])
    variables = range(0, len(cols) + 1)
    colnames  = ['eid'] + ['{}-0.0'.format(v) for v in variables[1:]]

    columns = collections.OrderedDict(zip(colnames[1:], cols))

    data = pd.DataFrame(columns)
    data['eid'] = np.arange(1, nsubjs + 1)
    data.set_index('eid', inplace=True)

    return gen_DataTableFromDataFrame(data, *a, **kwa)


def gen_DataTableFromDataFrame(df, tables=None, pool=None):

    variables = list(range(1, len(df.columns) + 1))
    colobjs   = [datatable.Column(None, df.index.name, 0, 0, 0, 0)] + \
                [datatable.Column(None, n, v, v, 0, 0)
                 for v, n in zip(variables, df.columns)]

    if tables is None:
        vartable, proctable, cattable, uvs = gen_tables(variables)
    else:
        vartable, proctable, cattable = tables

    return datatable.DataTable(df, colobjs, vartable, proctable, cattable,
                               pool=pool)
