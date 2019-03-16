#!/usr/bin/env python
#
# join.py - join variable/datacoding tsv files
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""Generate the variable and data coding files by performing a left
join on the base files.

Each input file must:
   - be tab-separated (``.tsv``) files,
   - with the first line containing column names,
   - and an ``ID`` column on which to join with the other input files.

The output file will contain a row for every row in the *first* input file.

The variable and data coding table files are generated by a set of "base"
files, which are easier to manage::

    ukbparse/data/variables_base.tsv
    ukbparse/data/variables_navalues.tsv
    ukbparse/data/variables_recoding.tsv
    ukbparse/data/variables_parentvalues.tsv
    ukbparse/data/variables_clean.tsv
    ukbparse/data/datacodings_base.tsv
    ukbparse/data/datacodings_navalues.tsv
    ukbparse/data/datacodings_recoding.tsv

The variable table can be (re-)generated via::

    python scripts/join.py ukbparse/data/variables.tsv \\
                           ukbparse/data/variables_base.tsv \\
                           ukbparse/data/variables_navalues.tsv \\
                           ukbparse/data/variables_recoding.tsv \\
                           ukbparse/data/variables_parentvalues.tsv \\
                           ukbparse/data/variables_clean.tsv

And the data coding table can be (re-) generated like so::

    python scripts/join.py ukbparse/data/datacodings.tsv \\
                           ukbparse/data/datacodings_base.tsv \\
                           ukbparse/data/datacodings_navalues.tsv \\
                           ukbparse/data/datacodings_recoding.tsv
"""


import sys
import itertools as it

import numpy  as np
import pandas as pd


in_dtypes = {
    'Index'        : np.uint32,
    'ID'           : np.uint32,
    'Type'         : str,
    'Description'  : str,
    'DataCoding'   : np.float32,
    'NAValues'     : str,
    'RawLevels'    : str,
    'NewLevels'    : str,
    'ParentValues' : str,
    'ChildValues'  : str,
}


def fmtInt(v):
    try:              return str(int(v))
    except Exception: return ''


def fmtOther(v):
    if v is np.nan: return ''
    else:           return str(v)


out_fmts = {
    'DataCoding' : fmtInt,
}


def join(series):
    base = series[0]
    return base.join(series[1:])


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    if len(args) < 2:
        print('Usage: join outfile infile infile ...')
        print()
        print(__doc__)
        sys.exit(0)

    outfile = args[0]
    infiles = args[1:]
    series  = [pd.read_csv(f, '\t', index_col='ID', dtype=in_dtypes)
               for f in infiles]

    # preserve column ordering (including index)
    with open(infiles[0], 'rt') as f:
        columns = list(f.readline().strip().split('\t'))
    columns.extend(list(it.chain(*[s.columns for s in series[1:]])))

    # do the join
    joined = join(series)

    # turn index into a regular column
    joined['ID'] = joined.index

    data = [joined[c] for c in columns]

    with open(outfile, 'wt') as f:
        f.write('\t'.join(columns) + '\n')

        for rowi in range(len(data[0])):
            rowelems = []
            for name, col in zip(columns, data):
                val = col.iloc[rowi]
                fmt = out_fmts.get(name, fmtOther)
                rowelems.append(fmt(val))

            f.write('\t'.join(rowelems) + '\n')


if __name__ == '__main__':
    main()
