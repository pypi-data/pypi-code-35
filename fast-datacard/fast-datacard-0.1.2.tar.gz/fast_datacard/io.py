import ast
import errno
import operator
import os
import re

import pandas as pd


def custom_pd_read_table(path, dtype=None):
    """
    From https://gitlab.cern.ch/fast-cms/FAST-RA1/blob/master/external/aggregate/aggregate/files.py#L27
    read a data frame from a file with all columns as categories
    unless other types are specified.

    dtype : e.g., {'n': float, 'nvar': float}

    """
    if dtype is None:
        dtype = {}

    try:
        columns = open(path).readline().split()
    except TypeError:  # path is buffer
        columns = path.readline().split()
        path.seek(0)
    # e.g, columns = ['component', 'cutflow', 'bintype', 'nJet100', 'n', 'nvar']

    columns_specified = dtype.keys()
    # e.g. ['nvar', 'n']

    str_columns = [c for c in columns if c not in columns_specified]
    # e.g, ['component', 'cutflow', 'bintype', 'nJet100']

    column_type_dict = dtype.copy()
    column_type_dict.update(dict([(c, str) for c in str_columns]))
    # e.g. {'component': <type 'str'>, 'nJet100': <type 'str'>, 'nvar': <type
    # 'float'>, 'cutflow': <type 'str'>, 'bintype': <type 'str'>, 'n': <type
    # 'float'>}

    tbl = pd.read_table(path, delim_whitespace=True, dtype=column_type_dict)

    return convert_column_types_to_category(tbl, str_columns)


def convert_column_types_to_category(tbl, columns):
    """
        From https://gitlab.cern.ch/fast-cms/FAST-RA1/blob/master/external/aggregate/aggregate/dtype.py#L28
    """
    tbl = tbl.copy()

    # http://pandas.pydata.org/pandas-docs/stable/categorical.html
    for c in columns:
        if c not in tbl.columns:
            continue

        # tbl[c] = tbl[:][c].astype(pd.api.types.CategoricalDtype(categories=list(c)), ordered=True)

        try:
            tbl[c] = tbl[c].astype(CategoricalDtype(ordered=True))
        except (NameError, TypeError):
            # for pandas older than 0.21
            tbl[c] = tbl[:][c].astype('category', ordered=True)
            # not clear why.  but without '[:]', sometime 'ordered' is not effective

        # tbl[c] = tbl[:][c].astype('category', ordered=True)
        # not clear why.  but without '[:]', sometime 'ordered' is not effective

        try:
            # order numerically if numeric
            categories = [(e, ast.literal_eval(str(e)))
                          for e in tbl[c].cat.categories]
            # e.g., [('100.47', 100.47), ('15.92', 15.92), ('2.0', 2.0)]

            categories = sorted(categories, key=operator.itemgetter(1))
            # e.g., [('2.0', 2.0), ('15.92', 15.92), ('100.47', 100.47)]

            categories = [e[0] for e in categories]
            # e.g., ['2.0', '15.92', '100.47']

        except BaseException:
            # alphanumeric sort
            categories = sorted(tbl[c].cat.categories, key=lambda n: [float(
                c) if c.isdigit() else c for c in re.findall('\d+|\D+', n)])

        tbl[c].cat.reorder_categories(categories, ordered=True, inplace=True)

    return tbl


def mkdir_p(path):
    """
        From http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise exc
