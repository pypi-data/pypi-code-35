#!/usr/bin/env python
#
# loadtables.py - Functions which load the variable, data coding, processing,
#                 and category tables used by ukbparse.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module provides functions and logic to load the variable, data coding,
processing, and category tables used by ukbparse:


.. autosummary::
   :nosignatures:

   loadTables
   loadDefaultTables
   loadVariableTable
   addNewVariable
   loadProcessingTable
   loadCategoryTable
   categoryVariables
   columnTypes
"""


import itertools as it
import              re
import              logging
import              warnings
import              functools
import              collections

import numpy  as np
import pandas as pd

from . import util
from . import fileinfo
from . import processing
from . import expression


log = logging.getLogger(__name__)


def convert_type(val):
    """Convert a string containing a type into a numerical identifier for that
    type.
    """
    valmap = {
        'sequence' :
        util.CTYPES.sequence,
        'integer' :
        util.CTYPES.integer,
        'continuous' :
        util.CTYPES.continuous,
        'categorical (single)' :
        util.CTYPES.categorical_single,
        'categorical (single non-numeric)' :
        util.CTYPES.categorical_single_non_numeric,
        'categorical (multiple)' :
        util.CTYPES.categorical_multiple,
        'categorical (multiple non-numeric)' :
        util.CTYPES.categorical_multiple_non_numeric,
        'time' : util.CTYPES.time,
        'date' :
        util.CTYPES.date,
        'text' :
        util.CTYPES.text,
        'compound' :
        util.CTYPES.compound,
        'unknown' :
        util.CTYPES.unknown,
    }
    return valmap.get(val.lower(), util.CTYPES.unknown)


def convert_comma_sep_text(val):
    """Convert a string containing comma-separated text into a list. """
    if val.strip() == '':
        return np.nan
    words = val.split(',')
    return [w.strip() for w in words]


def convert_comma_sep_numbers(val):
    """Convert a string containing comma-separated numbers into a ``numpy``
    array.
    """
    if val.strip() == '':
        return np.nan
    return np.fromstring(val, sep=',', dtype=np.float)


def convert_ParentValues(val):
    """Convert a string containing a sequence of comma-separated
    ``ParentValue`` expressions into a sequence of :class:`.Expression`
    objects.
    """
    if val.strip() == '':
        return np.nan
    return [expression.Expression(e) for e in val.split(',')]


def convert_Process_Variable(val):
    """Convert a string containing a process variable specification - one of:

      - ``'all'``, indicating that the process is to be applied to all
        variables simultaneously

      - ``'all_independent'``,, indicating that the process is to be applied
        to all variables independently

      - One or more comma-separated MATLAB-style ``start:stop:step`` ranges.
    """
    if val in ('all', 'all_independent'):
        return val
    else:
        tokens = convert_comma_sep_text(val)
        return list(it.chain(*[util.parseMatlabRange(t) for t in tokens]))


def convert_Process(ptype, val):
    """Convert a string containing a sequence of comma-separated ``Process`` or
    ``Clean`` expressions into an ``OrderedDict`` of :class:`.Process`
    objects (with the process names used as dictionary keys).
    """
    if val.strip() == '':
        return np.nan

    procs = processing.parseProcesses(val, ptype)

    return collections.OrderedDict([(p.name, p)  for p in procs])


def convert_category_variables(val):
    """Convert a string containing a sequence of comma-separated variable IDs
    or ranges into a list of variable IDs. Variables may be specified as
    integer IDs, or via a MATLAB-style ``start:step:stop`` range. See
    :func:`.util.parseMatlabRange`.
    """

    ranges    = convert_comma_sep_text(val)
    variables = list(it.chain(*[util.parseMatlabRange(r) for r in ranges]))

    return variables


VARTABLE_COLUMNS = [
    'ID',
    'Type',
    'Description',
    'DataCoding',
    'NAValues',
    'RawLevels',
    'NewLevels',
    'ParentValues',
    'ChildValues',
    'Clean']
"""The columns that must be in a variable table file. """


DCTABLE_COLUMNS = [
    'ID',
    'NAValues',
    'RawLevels',
    'NewLevels']
"""The columns that must be in a datacoding table file. """


TYPETABLE_COLUMNS = [
    'Type',
    'Clean']
"""The columns that must be in a type table file. """


PROCTABLE_COLUMNS = [
    'Variable',
    'Process']
"""The columns that must be in a processing table file. """


CATTABLE_COLUMNS = [
    'ID',
    'Category',
    'Variables']
"""The columns that must be in a category table file. """


VARTABLE_DTYPES = {
    'ID'           : np.uint32,
    'Description'  : object,

    # We can't use an integer for the data
    # coding, because not all variables
    # have a data coding, and pandas uses
    # np.nan to represent missing data.
    'DataCoding'   : np.float32,
    'NAValues'     : object,
    'RawLevels'    : object,
    'NewLevels'    : object,
    'ParentValues' : object,
    'ChildValues'  : object,
    'Clean'        : object,

}
"""Types to use for some columns in the variable table. """


VARTABLE_CONVERTERS = {
    'Type'         : convert_type,
    'NAValues'     : convert_comma_sep_numbers,
    'RawLevels'    : convert_comma_sep_numbers,
    'NewLevels'    : convert_comma_sep_numbers,
    'ParentValues' : convert_ParentValues,
    'ChildValues'  : convert_comma_sep_numbers,
    'Clean'        : functools.partial(convert_Process, 'cleaner'),
}
"""Custom converter functinos to use for some columns in the variable
table.
"""


DCTABLE_DTYPES = {
    'ID'         : np.uint32,
    'NAValues'   : object,
    'RawLevels'  : object,
    'NewLevels'  : object,
}
"""Types to use for some columns in the data coding table. """


DCTABLE_CONVERTERS = {
    'NAValues'  : convert_comma_sep_numbers,
    'RawLevels' : convert_comma_sep_numbers,
    'NewLevels' : convert_comma_sep_numbers,
}
"""Custom converter functinos to use for some columns in the data coding
table.
"""


TYPETABLE_DTYPES = {
    'Type'  : object,
    'Clean' : object,
}
"""Types to use for some columns in the types table. """


TYPETABLE_CONVERTERS = {
    'Type'  : convert_type,
    'Clean' : functools.partial(convert_Process, 'cleaner'),
}
"""Custom converter functinos to use for some columns in the type trable. """



PROCTABLE_CONVERTERS = {
    'Variable' : convert_Process_Variable,
    'Process'  : functools.partial(convert_Process, 'processor'),
}
"""Custom converter functinos to use for some columns in the processing
table.
"""


CATTABLE_DTYPES = {
    'ID' : np.int32,
}
"""Types to use for some columns in the category table. """


CATTABLE_CONVERTERS = {
    'Variables' : convert_category_variables
}
"""Custom converter functinos to use for some columns in the category
table.
"""

UNKNOWN_CATEGORY_ID = -1
"""Category table ID to use for the automatically added unknown variable
category.
"""



def loadTables(datafiles,
               varfile,
               dcfile,
               typefile,
               procfile,
               catfile,
               **kw):
    """Loads the data tables used to run ``ukbparse``.

    :arg datafiles: Path(s) to the data files
    :arg varfile:   Path to the variable table file
    :arg dcfile:    Path to the data coding table file
    :arg typefile:  Path to the type table file
    :arg procfile:  Path to the processing table file
    :arg catfile:   Path to the category table file

    All other arguments are passed throughh to the :func:`loadVariableTable`
    and :func:`loadProcessingTable` functions.

    :returns:      A tuple containing:
                    - The variable table
                    - The processing table
                    - The category table
                    - List of integer variable IDs which are present in the
                      data, but were not present in the variable table.
    """

    vartable, uvs = loadVariableTable(datafiles,
                                      varfile,
                                      dcfile,
                                      typefile,
                                      **kw)
    proctable     = loadProcessingTable(procfile, **kw)
    cattable      = loadCategoryTable(catfile, uvs)

    return vartable, proctable, cattable, uvs


def loadDefaultTables(datafiles, **kw):
    """Convenience variant of :func:`loadTables` which uses the default
    table files.
    """

    from . import config
    return loadTables(datafiles,
                      config.DEFAULT_VFILE,
                      config.DEFAULT_DFILE,
                      config.DEFAULT_TFILE,
                      config.DEFAULT_PFILE,
                      config.DEFAULT_CFILE,
                      **kw)


def loadVariableTable(datafiles,
                      varfile=None,
                      dcfile=None,
                      typefile=None,
                      naValues=None,
                      childValues=None,
                      recoding=None,
                      clean=None,
                      typeClean=None,
                      globalClean=None,
                      indexes=None,
                      sniffers=None,
                      dropAbsent=True,
                      **kwargs):
    """Given variable table and datacoding table file names, builds and returns
    the variable table.


    TODO describe how dcfile/typefile are merged.

    :arg datafiles:   Path(s) to the data files

    :arg varfile:     Path to the variable file

    :arg dcfile:      Path to the data coding file

    :arg typefile:    Path to the type file

    :arg naValues:    Dictionary of ``{vid : [values]}`` mappings, specifying
                      values which should be replaced with NA.

    :arg childValues: Dictionary of ``{vid : [exprs], [values]}`` mappings,
                      specifying parent value expressions, and corresponding
                      child values.

    :arg recoding:    Dictionary of ``{vid : [rawlevel], [newlevel]}``
                      mappings

    :arg clean:       Dictionary of ``{vid : expr}`` mappings containing
                      cleaning functions to apply - this will override
                      any cleaning specified in the variable file, and
                      any cleaning specified in ``typeClean``.

    :arg typeClean:   Dictionary of ``{type : expr}`` mappings containing
                      cleaning functions to apply to all variables of a
                      specific type - this will override any cleaning
                      specified in the type file.

    :arg globalClean: Expression containing cleaning functions to
                      apply to every variable - this will be performed after
                      variable-specific cleaning in the variable table,
                      or specified via ``clean`` or ``typeClean``.

    :arg indexes:     Dict of ``{filename : index}`` mappings, specifying
                      the number of the column to use as the index.
                      Defaults to 0 (the first column).

    :arg sniffers:    Dict of ``{ file : snifferName }`` mappings containing
                      custom sniffers to be used for specific files. See the
                      :mod:`.custom` module.

    :arg dropAbsent:  If ``True`` (the default), remove all variables from the
                      variable table which are not present in the data
                      file(s).

    All other keyword arguments are ignored.

    :returns: A tuple containing:

                - A ``pandas.DataFrame`` containing the variable table

                - A sequence of :class:`.Column` objects representing variables
                  which were present in the data files, but not in the variable
                  table, but were added to the variable table.
    """

    if sniffers is None: sniffers = {}
    if indexes  is None: indexes  = {}

    def load_table_file(fname, what, dtypes, converters, columns):

        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=pd.errors.ParserWarning)

            if fname is not None:
                log.debug('Loading %s table from %s', what, fname)
                table = pd.read_csv(fname, '\t',
                                    index_col=0,
                                    dtype=dtypes,
                                    converters=converters)
            else:
                table            = pd.DataFrame(columns=columns[1:])
                table.index.name = columns[0]

        if list(sorted(table.columns)) != sorted(columns[1:]):
            raise ValueError('Missing/unrecognised columns in table file {} - '
                             'should be {}, but file contained {}.'.format(
                                 fname, columns, table.columns))

        return table

    vartable = load_table_file(varfile,
                               'variable',
                               VARTABLE_DTYPES,
                               VARTABLE_CONVERTERS,
                               VARTABLE_COLUMNS)
    dctable  = load_table_file(dcfile,
                               'data coding',
                               DCTABLE_DTYPES,
                               DCTABLE_CONVERTERS,
                               DCTABLE_COLUMNS)
    tytable  = load_table_file(typefile,
                               'type',
                               TYPETABLE_DTYPES,
                               TYPETABLE_CONVERTERS,
                               TYPETABLE_COLUMNS)

    # Make sure data types are aligned,
    # otherwise we may run into problems
    # when merging them together.
    vartable = vartable.astype(
        {c : t for c, t in VARTABLE_DTYPES .items() if c != 'ID'})
    dctable  = dctable .astype(
        {c : t for c, t in DCTABLE_DTYPES  .items() if c != 'ID'})
    tytable  = tytable .astype(
        {c : t for c, t in TYPETABLE_DTYPES.items() if c != 'Type'})

    vartable.index = vartable.index.astype(VARTABLE_DTYPES[ 'ID'])
    dctable .index = dctable .index.astype(DCTABLE_DTYPES[  'ID'])
    tytable .index = tytable .index.astype(TYPETABLE_DTYPES['Type'])

    # All column names and variable
    # IDs in the input data files
    finfo = fileinfo.fileinfo(datafiles,
                              indexes=indexes,
                              sniffers=sniffers)

    # with the index column from
    # each file dropped
    cols = list(finfo[2])
    for i, df in enumerate(datafiles):
        idxcol  = indexes.get(df, 0)
        cols[i] = cols[i][:idxcol] + cols[i][idxcol + 1:]
    cols = list(it.chain(*cols))

    # Make sure the variable table
    # contains an entry for every
    # variable in the input data.
    unknownVars = _sanitiseVariableTable(vartable, cols, dropAbsent)

    # Merge data coding specific NAValues,
    # RawLevels, and NewLevels from the data
    # coding table into the variable table.
    _mergeDataCodingTable(vartable, dctable)

    # Merge provided naValues, recodings,
    # and childValues into the variable
    # table (overriding whatever was specified
    # in the datacoding/variable tables)
    if naValues is not None:
        naValues = {vid : np.array(vals) for vid, vals in naValues.items()}
        _mergeIntoVariableTable(
            vartable,
            'NAValues',
            naValues)

    if recoding is not None:
        recoding = {vid : (np.array(raw), np.array(new))
                    for vid, (raw, new) in recoding.items()}
        _mergeIntoVariableTable(
            vartable,
            ['RawLevels', 'NewLevels'],
            recoding)

    if childValues is not None:
        childValues = {vid : (convert_ParentValues(expr),
                              np.array(values))
                       for vid, (expr, values) in childValues.items()}
        _mergeIntoVariableTable(
            vartable,
            ['ParentValues', 'ChildValues'],
            childValues)

    # Merge clean options into variable table
    _mergeCleanFunctions(vartable, tytable, clean, typeClean, globalClean)

    return vartable, unknownVars


def _sanitiseVariableTable(vartable, cols, dropAbsent):
    """Ensures that the variable table contains an entry for every
    variable in the input data.

    Called by :func:`loadVariableTable`.

    :arg vartable:   ``pandas.DataFrame`` containing the variable table.

    :arg cols:       Sequence of :class:`.Column` objects representing
                     the columns in the input data.

    :arg dropAbsent: If ``True``, entries in the table for variables which are
                     not in ``cols`` will be removed.

    :return:         A list of unknown :class:`.Column` objects, i.e.
                     representing variables which were not in the variable
                     table.
    """

    unknownVars = []

    # Make sure a placeholder entry is
    # present for any variables which are
    # not in the variable table, but which
    # are in the data file(s).
    for i, col in enumerate(cols):

        vid  = col.vid
        name = col.name

        if vid in vartable.index:
            continue

        unknownVars.append(col)
        addNewVariable(vartable, vid, name)

    # And the inverse - we can drop any
    # variables from the variable table
    # that are not in the data.
    if dropAbsent:
        vids = [c.vid for c in cols]
        vartable.drop([v for v in vartable.index if v not in vids],
                      inplace=True)
    return unknownVars


def _mergeIntoVariableTable(vartable, cols, mapping):
    """Merge data from ``mapping`` into the variable table.

    Called by :func:`loadVariableTable`.

    :arg vartable: The variable table

    :arg cols:     Names of columns in the variable table

    :arg mapping:  Dict of ``{vid : values}`` mappings containing the
                   data to copy in.
    """

    onecol = isinstance(cols, str)
    if onecol:
        cols = [cols]

    # Ignore any variables that
    # are not in variable table
    vids   = list(mapping.keys())
    vin    = pd.Series(vids).isin(vartable.index)
    vids   = [v for i, v in enumerate(vids) if vin[i]]

    for vid in vids:
        vals = mapping[vid]

        if onecol:
            vals = [vals]

        for col, val in zip(cols, vals):
            vartable.at[vid, col] = val


def _mergeDataCodingTable(vartable, dctable):
    """Merges information from the data coding table into the variable
    table.

    Called by :func:`loadVariableTable`.

    :arg vartable: The variable table.
    :arg dctable:  The data coding table.
    """

    with_datacoding = vartable['DataCoding'].notna()

    for field in ['NAValues', 'RawLevels', 'NewLevels']:
        mask    = vartable[field].isna() & with_datacoding
        newvals = vartable.loc[mask].merge(dctable,
                                           left_on='DataCoding',
                                           right_index=True,
                                           suffixes=('_v', '_dc'),
                                           copy=False)['{}_dc'.format(field)]
        vartable.loc[mask, field] = newvals


def _mergeCleanFunctions(vartable, tytable, clean, typeClean, globalClean):
    """Merges custom clean functions into the variable table.

    Called by :func:`loadVariableTable`.

    :arg vartable:    The variable table.

    :arg tytable:     The type table

    :arg clean:       Dictionary of ``{vid : expr}`` mappings containing
                      cleaning functions to apply - this will override
                      any cleaning specified in the variable file, and
                      any cleaning specified in ``typeClean``.

    :arg typeClean:   Dictionary of ``{type : expr}`` mappings containing
                      cleaning functions to apply to all variables of a
                      specific type - this will override any cleaning
                      specified in the type file.

    :arg globalClean: Expression containing cleaning functions to
                      apply to every variable - this will be performed after
                      variable-specific cleaning in the variable table,
                      or specified via ``clean`` or ``typeClean``.
    """

    # Merge type-specific Clean
    # from the type table into
    # the variable table.
    for vid in vartable.index:

        if vid == 0:
            continue

        vtype = vartable.loc[vid, 'Type']
        pp    = vartable.loc[vid, 'Clean']

        # Override with typeClean if necessary
        if typeClean is not None and vtype in typeClean:
            tpp = convert_Process('cleaner', typeClean[vtype])
        elif vtype in tytable.index:
            tpp = collections.OrderedDict((tytable.loc[vtype, 'Clean']))
        else:
            continue

        # type cleaning is applied after
        # variable-specific cleaning
        if pd.isnull(pp): vartable.loc[[vid], 'Clean'] = [tpp]
        else:             vartable.loc[ vid,  'Clean'].update(tpp)

    # Override cleaning with expressions
    # that have been passed on the command line
    if clean is not None:
        clean = {vid : convert_Process('cleaner', expr)
                 for vid, expr in clean.items()}
        _mergeIntoVariableTable(vartable, 'Clean', clean)

    # Add global cleaning to all variables
    if globalClean is not None:

        for vid in vartable.index:

            if vid == 0:
                continue

            pp  = vartable.loc[vid, 'Clean']
            gpp = convert_Process('cleaner', globalClean)

            # global cleaning is applied
            # after all other cleaning
            if pd.isnull(pp): vartable.loc[[vid], 'Clean'] = [gpp]
            else:             vartable.loc[ vid,  'Clean'].update(gpp)


def addNewVariable(vartable, vid, name, dtype=None):
    """Add a new row to the variable table.

    :arg vartable: The variable table
    :arg vid:      Integer variable ID
    :arg name:     Variable name - used as the description
    :arg dtype:    ``numpy`` data type. If ``None``, the variable type
                   is set to :attr:`.util.CTYPES.unknown`.
    """

    # set dtype to something which
    # will cause the conditionals
    # to fall through
    if dtype is None: dtype = object
    else:             dtype = dtype.type

    if   issubclass(dtype, np.integer): dtype = util.CTYPES.integer
    elif issubclass(dtype, np.float):   dtype = util.CTYPES.continuous
    else:                               dtype = util.CTYPES.unknown

    vartable.loc[vid, 'Description'] = name
    vartable.loc[vid, 'Type']        = dtype


def loadProcessingTable(procfile=None,
                        skipProcessing=False,
                        prependProcess=None,
                        appendProcess=None,
                        **kwargs):
    """Loads the processing table from the given file.

    :arg procfile:       Path to the processing table file.

    :arg skipProcessing: If ``True``, the processing table is not loaded from
                         ``procfile``. The ``prependProcess`` and
                         ``appendProcess`` arguments are still applied.

    :arg prependProcess: Sequence of ``(varids, procstr)`` mappings specifying
                         processes to prepend to the beginning of the
                         processing table.

    :arg appendProcess:  Sequence of ``(varids, procstr)`` mappings specifying
                         processes to append to the end of the processing
                         table.

    All other keyword arguments are ignored.
    """

    if prependProcess is None: prependProcess = []
    if appendProcess  is None: appendProcess  = []

    if (procfile is not None) and (not skipProcessing):
        log.debug('Loading processing table from %s', procfile)
        proctable = pd.read_csv(procfile, '\t',
                                index_col=False,
                                converters=PROCTABLE_CONVERTERS)

    else:
        proctable = pd.DataFrame(columns=PROCTABLE_COLUMNS)

    # prepend/append custom
    # processes to the table
    proctable.index += len(prependProcess)
    for i, (vids, procs) in enumerate(prependProcess):
        vids  = convert_Process_Variable(vids)
        procs = convert_Process('processor', procs)
        proctable.loc[i, ['Variable', 'Process']] = [vids, procs]

    for i, (vids, procs) in enumerate(appendProcess, len(proctable.index)):
        vids  = convert_Process_Variable(vids)
        procs = convert_Process('processor', procs)
        proctable.loc[i, ['Variable', 'Process']] = [vids, procs]

    proctable.sort_index(inplace=True)

    return proctable


def loadCategoryTable(catfile=None, unknownVars=None):
    """Loads the category table from the given file.

    :arg catfile:     Path to the category file.
    :arg unknownVars: Sequence of :class:`.Column` objects representing
                      variables to add to an "unknown" category.
    """
    if catfile is not None:
        log.debug('Loading category table from %s', catfile)
        cattable = pd.read_csv(catfile,
                               '\t',
                               index_col=0,
                               dtype=CATTABLE_DTYPES,
                               converters=CATTABLE_CONVERTERS)
    else:
        cattable            = pd.DataFrame(columns=CATTABLE_COLUMNS[1:])
        cattable.index.name = CATTABLE_COLUMNS[0]

    # add an implicit "unknown" category
    # for any columns in the data file
    # which are unknown
    if unknownVars is not None:

        unknownVids = list(sorted(set([c.vid for c in unknownVars])))

        # unknown column already in table?
        umask = cattable['Category'] == 'unknown'

        if np.any(umask):
            idx         = np.where(umask)[0][0]
            idx         = cattable.index[idx]
            unknownVids = cattable.loc[idx, 'Variables'] + unknownVids
        else:
            idx = UNKNOWN_CATEGORY_ID

        cattable.loc[idx, 'Category']  = 'unknown'
        cattable.loc[idx, 'Variables'] = list(unknownVids)

    return cattable


def categoryVariables(cattable, categories):
    """Returns a list of variable IDs from ``cattable`` which correspond to
    the strings in ``categories``.

    :arg cattable:   The category table.
    :arg categories: Sequence of integer category IDs or label sub-strings
                     specifying the categories to return.
    :returns:        A list of variable IDs as strings.
    """

    allvars = []

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        for cat in categories:

            catpat  = re.compile('({})'.format(cat), re.IGNORECASE)
            idmask  = cattable.index.isin([cat])
            lblmask = cattable['Category'].str.contains(catpat)
            catvars = cattable.loc[idmask | lblmask, 'Variables']

            if len(catvars) == 0:
                continue

            for c in catvars.iloc[0]:
                if c not in allvars:
                    allvars.append(c)

    return allvars


def columnTypes(vartable, columns):
    """Retrieves the type of each column in ``cols`` as listed in ``vartable``.
    Also identifies a suitable internal data type to use for each column where
    possible.

    :arg vartable: The variable table.

    :arg columnss: List of :class:`.Column` objects.

    :returns:      A tuple containing:

                    - A list containing the type for each column in ``cols`` -
                      an identifier from the :attr:`.util.CTYPES` enum.
                      Columns corresponding to a variable which is not in
                      the variable table is given a type of ``None``.

                    - A dict of ``{ column_name : dtype }`` mappings containing
                      a suitable internal data type to use for some columns.
    """

    vttypes = []
    dtypes  = {}

    for col in columns:

        vid  = col.vid
        name = col.name

        if vid not in vartable.index:
            vttypes.append(None)
            continue

        vttype = vartable.loc[vid, 'Type']
        dtype  = util.DATA_TYPES.get(vttype, None)

        vttypes.append(vttype)
        if dtype is not None:
            dtypes[name] = dtype

    return vttypes, dtypes
