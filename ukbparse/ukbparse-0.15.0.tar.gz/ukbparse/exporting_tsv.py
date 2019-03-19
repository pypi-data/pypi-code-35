#!/usr/bin/env python
#
# exporting_tsv.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import logging

import numpy            as np
import pandas           as pd
import pandas.api.types as pdtypes

from . import util
from . import custom


log = logging.getLogger(__name__)


TSV_SEP = '\t'
"""Default separator string to use in TSV-style output files."""


@custom.exporter('tsv')
def exportTSV(dtable,
              outfile,
              subjects,
              idcol,
              colnames,
              sep=None,
              missingValues=None,
              dateFormat=None,
              timeFormat=None,
              formatters=None,
              numRows=None,
              **kwargs):
    """Export data to a TSV-style file.

    :arg dtable:        :class:`.DataTable` containing the data

    :arg outfile:       File to output to

    :arg subjects:      Sequence containing subjects (and order) to export.

    :arg idcol:         Name to use for the subject ID column

    :arg colnames:      Sequence containing column names

    :arg sep:           Separator character to use. Defaults to
                        :attr:`TSV_SEP`

    :arg missingValues: String to use for missing/NA values. Defaults to the
                        empty string.

    :arg dateFormat:    Name of formatter to use for date columns.

    :arg timeFormat:    Name of formatter to use for time columns.

    :arg formatters:    Dict of ``{ vid : formatter }`` mappings, specifying
                        custom formatters to use for specific variables.

    :arg numRows:       Number of rows to write at a time. Defaults to writing
                        all rows in one go.
    """
    if sep           is None: sep           = TSV_SEP
    if missingValues is None: missingValues = ''
    if dateFormat    is None: dateFormat    = 'default'
    if timeFormat    is None: timeFormat    = 'default'
    if formatters    is None: formatters    = {}
    if numRows       is None: numRows       = len(dtable)
    if colnames      is None: colnames      = True

    nchunks   = int(np.ceil(len(subjects) / numRows))
    vartable  = dtable.vartable

    log.info('Writing %u columns in %u chunk(s) to %s ...',
             len(dtable.allColumns), nchunks, outfile)

    for chunki in range(nchunks):

        cstart  = chunki * numRows
        cend    = cstart + numRows
        csubjs  = subjects[cstart:cend]
        towrite = pd.DataFrame(index=csubjs)

        for col in dtable.allColumns:

            vid = col.vid

            if vid == 0:
                continue

            name      = col.name
            series    = dtable[csubjs, name]
            formatter = formatters.get(vid, None)

            if vid in vartable.index: vtype = vartable['Type'][vid]
            else:                     vtype = None

            # allow formatters to be
            # specified by column name
            # as well
            if formatter is None:
                formatter = formatters.get(name, None)

            # fall back to date/time formatting
            # if relevant for this column
            if formatter is None:
                if   vtype == util.CTYPES.date:
                    formatter = dateFormat
                elif vtype == util.CTYPES.time or \
                     pdtypes.is_datetime64_any_dtype(series):
                    formatter = timeFormat

            if formatter is not None:
                log.debug('Formatting column %s [chunk %u] with %s formatter',
                          name, chunki, formatter)
                towrite[name] = custom.runFormatter(
                    formatter, dtable, col, series)
            else:
                towrite[name] = series

        if chunki > 0:
            mode        = 'a'
            header      = False
            index_label = None
        else:
            mode        = 'w'
            header      = colnames
            index_label = idcol

        towrite.to_csv(outfile,
                       sep=sep,
                       na_rep=missingValues,
                       header=header,
                       index_label=index_label,
                       mode=mode)
