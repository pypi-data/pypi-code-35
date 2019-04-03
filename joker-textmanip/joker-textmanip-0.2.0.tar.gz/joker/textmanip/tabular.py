#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import collections


def _split2(s):
    parts = s.strip().split(None, 1)
    while len(parts) < 2:
        parts.append(None)
    return tuple(parts)


def text_to_dict(lines, reverse=False):
    if isinstance(lines, str):
        lines = lines.splitlines()
    tups = [_split2(x) for x in lines]
    if reverse:
        tups = [tu[::-1] for tu in tups]
    # print('debug: tups', tups)
    return collections.OrderedDict(tups)


def textfile_to_dict(path, reverse=False):
    from joker.cast.iterative import nonblank_lines_of
    return text_to_dict(nonblank_lines_of(path), reverse=reverse)


def dataframe_to_dicts(df):
    """
    :param df: (pandas.DataFrame)
    :return: (list) a list of dicts, each for a row of the dataframe
    """
    return list(df.T.to_dict().values())


def tabular_format(rows):
    from joker.cast import numerify
    from joker.textmanip import align
    rowcount = 0
    columns = collections.defaultdict(list)
    columntypes = collections.defaultdict(set)
    for row in rows:
        rowcount += 1
        for ic, cell in enumerate(row):
            cell = numerify(str(cell))
            columns[ic].append(cell)
            columntypes[ic].add(type(cell))

    types = [str, float, int]
    for ic in range(len(columns)):
        type_ = str
        for type_ in types:
            if type_ in columntypes[ic]:
                break
        if type_ == float:
            columns[ic] = align.text_align_for_floats(columns[ic])
        if type_ == int:
            just_method = 'rjust'
        else:
            just_method = 'ljust'
        columns[ic] = align.text_equal_width(columns[ic], method=just_method)
        print(ic, columns[ic])

    rows = []
    for ir in range(rowcount):
        row = []
        for ic in range(len(columns)):
            row.append(columns[ic][ir])
        rows.append(row)
    return rows
