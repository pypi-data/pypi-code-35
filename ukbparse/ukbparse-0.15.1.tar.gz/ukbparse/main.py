#!/usr/bin/env python
#
# main.py - ukbparse entry point
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains the ``ukbparse`` entry point. """


import multiprocessing as mp
import                    sys
import                    shutil
import                    logging
import                    fnmatch
import                    tempfile
import                    warnings
import                    datetime
import                    calendar

import ukbparse
import ukbparse.util       as util
import ukbparse.icd10      as icd10
import ukbparse.config     as config
import ukbparse.custom     as custom
import ukbparse.dryrun     as dryrun
import ukbparse.cleaning   as cleaning
import ukbparse.importing  as importing
import ukbparse.exporting  as exporting
import ukbparse.hierarchy  as hierarchy
import ukbparse.processing as processing
import ukbparse.loadtables as loadtables


log = logging.getLogger(__name__)


def main(argv=None):
    """``ukbparse`` entry point. """

    # Make sure built in plugins are
    # registered, as they are queried
    # in the command-line help. Set
    # logging to critical until we've
    # parsed command-line args.
    logging.getLogger().setLevel(logging.CRITICAL)
    custom.registerBuiltIns()

    args, argv = config.parseArgsWithConfigFile(argv)
    date = datetime.date.today()

    # Now that args are passed,
    # we can set up logging properly.
    configLogging(args)

    log.info('ukbparse %s', ukbparse.__version__)
    log.info('Date: %s (%s)', date.today(), calendar.day_name[date.weekday()])
    log.info('Command-line arguments %s', ' '.join(argv))
    log.debug('Running with the following options')
    for name, val in args.__dict__.items():
        if val is not None:
            val = str(val)
            if len(val) <= 30: log.debug('  %s: %s',    name, val)
            else:              log.debug('  %s: %s...', name, val[:30])

    # Re-load any custom plugins
    # that have been specified.
    custom.registerBuiltIns()

    if args.plugin_file is not None:
        for p in args.plugin_file:
            custom.loadPluginFile(p)

    # error if any loaders/formats are
    # invalid (we can only perform this
    # check after plugins have been
    # loaded)
    if args.loader is not None:
        for f, l in args.loader.items():
            if not custom.exists('loader', l):
                raise ValueError('Unknown loader {} [{}]'.format(l, f))
    if not custom.exists('exporter', args.format):
        raise ValueError('Unknown output format {}'.format(args.format))
    if args.date_format is not None and \
       not custom.exists('formatter', args.date_format):
        raise ValueError('Unknown date format {}'.format(args.date_format))
    if args.time_format is not None and \
       not custom.exists('formatter', args.time_format):
        raise ValueError('Unknown time format {}'.format(args.time_format))
    if args.tsv_var_format is not None:
        for v, f in args.tsv_var_format.items():
            if not custom.exists('formatter', f):
                raise ValueError('Unknown formatter {} [{}]'.format(f, v))

    if args.num_jobs > 1:
        log.debug('Running up to %i jobs in parallel', args.num_jobs)
        pool = mp.Pool(args.num_jobs)
        mgr  = mp.Manager()
    else:
        pool = None
        mgr  = None

    if args.work_dir is None: workdir = tempfile.mkdtemp(prefix='ukbparse')
    else:                     workdir = args.work_dir

    try:
        with util.timed(
                None, log, fmt='Total time: %i minutes, %i seconds (%+iMB)'):

            dtable, unknowns, drop = doImport(args, pool, mgr)

            if args.dry_run:
                dryrun.doDryRun(dtable, unknowns, drop, args)
            else:
                doCleanAndProcess(  dtable, args)
                finaliseColumns(    dtable, args, unknowns)
                doExport(           dtable, args)
                doICD10Export(              args)

    finally:
        # shutdown the pool gracefully
        if pool is not None:
            pool.close()
            pool.join()
            pool = None

        if args.work_dir is None:
            shutil.rmtree(workdir)
    return 0


def doImport(args, pool, mgr):
    """Data import stage.

    :arg args: :class:`argparse.Namespace` object containing command line
               arguments
    :arg pool: :class:`multiprocessing.Pool` object for parallelisation (may
               be ``None``)
    :arg mgr:  :class:`multiprocessing.Manager` object for parallelisation (may
               be ``None``)

    :returns:  A tuple containing:

                - A :class:`.DataTable` containing the data
                - A sequence of :class:`.Column` objects representing the
                  unknown columns.
    """

    with util.timed('Table import', log, minutes=False):
        vartable, proctable, cattable, unknowns = loadtables.loadTables(
            args.infile,
            args.variable_file,
            args.datacoding_file,
            args.type_file,
            args.processing_file,
            args.category_file,
            naValues=args.na_values,
            childValues=args.child_values,
            recoding=args.recoding,
            clean=args.clean,
            typeClean=args.type_clean,
            globalClean=args.global_clean,
            skipProcessing=args.skip_processing,
            prependProcess=args.prepend_process,
            appendProcess=args.append_process,
            sniffers=args.loader,
            indexes=args.index)

        for u in unknowns:
            log.warning('Detected unknown variable %s [file %s, column '
                        '%s, assigned variable ID %s]. Consider adding an '
                        'entry to the variable table', u.name, u.datafile,
                        u.index, u.vid)

    subjects, exprs = args.subject

    if not args.dry_run and args.import_all:
        variables     = None
        categories    = None
        columns       = None
        removeUnknown = None
    else:
        variables     = args.variable
        categories    = args.category
        columns       = args.column
        removeUnknown = args.remove_unknown

    # Import data
    with util.timed('Data import', log):
        dtable, drop = importing.importData(
            datafiles=args.infile,
            vartable=vartable,
            proctable=proctable,
            cattable=cattable,
            variables=variables,
            colnames=columns,
            categories=categories,
            subjects=subjects,
            encoding=args.encoding,
            indexes=args.index,
            unknownVars=unknowns,
            removeUnknown=removeUnknown,
            mergeAxis=args.merge_axis,
            mergeStrategy=args.merge_strategy,
            loaders=args.loader,
            lowMemory=args.low_memory,
            workDir=args.work_dir,
            pool=pool,
            mgr=mgr,
            dryrun=args.dry_run)

    # Exclude subjects
    if (not args.dry_run) and (exprs is not None or args.exclude is not None):
        with util.timed('Subject exclusion', log):
            importing.removeSubjects(
                dtable,
                exclude=args.exclude,
                exprs=exprs)

    return dtable, unknowns, drop


def doCleanAndProcess(dtable, args):
    """Data cleaning and processing stage.

    :arg dtable: :class:`.DataTable` containing the data
    :arg args:   :class:`argparse.Namespace` object containing command line
                 arguments
    :arg pool:   :class:`multiprocessing.Pool` object for parallelisation (may
                 be ``None``)
    """

    # Clean data (it times each step individually)
    cleaning.cleanData(
        dtable,
        skipNAInsertion=args.skip_insertna,
        skipCleanFuncs=args.skip_clean_funcs,
        skipChildValues=args.skip_childvalues,
        skipRecoding=args.skip_recoding)

    # Process data
    with util.timed('Data processing', log):
        processing.processData(dtable)


def finaliseColumns(dtable, args, unknowns):
    """Called after processing and before export.

    If the ``--import_all`` argument was used (which forces all columns
    to be loaded and processed), this function applies the ``--variable``,
    ``--category`` and ``--remove_unknown`` arguments. to the processed
    data.

    If the ``--unknown_vars_file`` argument was used, the unknown columns
    are saved out to a file.

    :arg dtable:   :class:`.DataTable` containing the data
    :arg args:     :class:`argparse.Namespace` object containing command line
                   arguments
    :arg unknowns: List of :class:`.Column` objects representing the
                   unknown columns.
    """

    if not args.import_all:
        return

    # get a list of variables requested
    # via --variable or --category (will
    # be None if no requests)
    vids = importing.restrictVariables(
        dtable.cattable, args.variable, args.category)

    # args.remove_unknown is only applied
    # if variables/columns were not already
    # restricted by args.variable,
    # args.category, and or args.column
    removeUnknown = all((vids is None,
                         args.remove_unknown,
                         args.column is None,
                         len(unknowns) > 0))

    # apply removeUnknown
    if removeUnknown:
        vids  = dtable.variables
        uvids = set([c.vid for c in unknowns])
        for vid in list(vids):
            if vid in uvids:
                vids.remove(vid)

    # apply column patterns
    if args.column is not None:
        remove = []
        for col in list(dtable.allColumns[1:]):
            hits = [fnmatch.fnmatch(col.name, pat) for pat in args.column]
            if not any(hits):
                remove.append(col)
        dtable.removeColumns(remove)

    # remove/reorder variables
    allcols = set([c.name for c in dtable.allColumns])
    if vids is None:
        finalcols = allcols
    else:
        vids = [vid for vid in vids if dtable.present(vid)]
        dtable.order(vids)
        finalcols = set([c.name for c in dtable.allColumns])

    # Save unknown vars list to file
    # columns:
    #  - name      - column name
    #  - file      - originating input file
    #  - processed - whether column passed processing
    #  - exported  - whether column was exported
    if args.unknown_vars_file is not None:
        names     = [    u.name               for u in unknowns]
        files     = [    u.datafile           for u in unknowns]
        processed = [int(u.name in allcols)   for u in unknowns]
        exported  = [int(u.name in finalcols) for u in unknowns]
        rows      = ['{}\t{}\t{}\t{}'.format(n, f, p, e)
                     for n, f, p, e in zip(names, files, processed, exported)]

        try:
            with open(args.unknown_vars_file, 'wt') as f:
                f.write('name\tfile\tprocessed\texported\n')
                f.write('\n'.join(rows))

        except Exception as e:
            log.warning('Error saving unknown variables to {}: '
                        '{}'.format(args.unknown_vars_file, e),
                        exc_info=True)


def doExport(dtable, args):
    """Data export stage.

    :arg dtable: :class:`.DataTable` containing the data
    :arg args:   :class:`argparse.Namespace` object containing command line
                 arguments
    """

    # Output data. Re-order subjects,
    # but only if no subject inclusion
    # expressions were used.
    subjects, exprs = args.subject

    if exprs is not None:
        subjects = None

    with util.timed('Data export', log):
        exporting.exportData(
            dtable,
            args.outfile,

            # General export options
            colpat=args.column_pattern,
            colmap=args.rename_column,
            idcol=args.output_id_column,
            fileFormat=args.format,
            dateFormat=args.date_format,
            timeFormat=args.time_format,
            numRows=args.num_rows,
            subjects=subjects,

            # TSV options
            sep=args.tsv_sep,
            missingValues=args.tsv_missing_values,
            formatters=args.tsv_var_format,

            # HDF5 options
            key=args.hdf5_key,
            style=args.hdf5_style)


def doICD10Export(args):
    """If a ``--icd10_map_file`` has been specified, the ICD10 codes present
    in the data (and their converted values) are saved out to the file.
    """
    if args.icd10_map_file is None:
        return

    with util.timed('ICD10 mapping export', log):
        try:
            ihier = hierarchy.loadHierarchyFile(args.icd10_file)
            icd10.saveCodes(args.icd10_map_file, ihier)

        except Exception as e:
            log.warning('Failed to export ICD10 mappings: {}'.format(e),
                        exc_info=True)


def configLogging(args):
    """Configures ``ukbparse`` logging.

    :arg args: ``argparse.Namespace`` object containing parsed command line
               arguments.
    """

    # Custom log handler which
    # colours messages
    class LogHandler(logging.StreamHandler):

        def emit(self, record):

            levelno = record.levelno

            if   levelno >= logging.WARNING:  colour = '\x1b[31;1m'
            elif levelno >= logging.INFO:     colour = '\x1b[39;1m'
            elif levelno >= logging.DEBUG:    colour = '\x1b[90;1m'
            else:                             colour = ''

            # Reset terminal attributes
            # after each message.
            record.msg = '{}{}\x1b[0m'.format(colour, record.msg)

            return super(LogHandler, self).emit(record)

    logger = logging.getLogger('ukbparse')
    fmt    = logging.Formatter('%(asctime)s '
                               '%(levelname)8.8s '
                               '%(filename)20.20s '
                               '%(lineno)4d: '
                               '%(funcName)-15.15s - '
                               '%(message)s',
                               '%H:%M:%S')

    if args.log_file is None: handler = LogHandler()
    else:                     handler = logging.FileHandler(args.log_file)

    handler.setFormatter(fmt)
    logger.addHandler(handler)

    # configure verbosity
    if   args.quiet:      loglevel = logging.CRITICAL
    elif args.noisy == 0: loglevel = logging.INFO
    else:                 loglevel = logging.DEBUG

    logging.getLogger('ukbparse').setLevel(loglevel)

    if args.quiet or args.noisy < 3:
        warnings.filterwarnings('ignore',  module='pandas')
        warnings.filterwarnings('ignore',  module='numpy')
        warnings.filterwarnings('ignore',  module='tables')

    if args.noisy == 1:
        makequiet = ['ukbparse.expression',
                     'ukbparse.custom',
                     'ukbparse.cleaning_functions',
                     'ukbparse.processing_functions']
    elif args.noisy == 2:
        makequiet = ['ukbparse.expression',
                     'ukbparse.custom']
    else:
        makequiet = []

    for mod in makequiet:
        logging.getLogger(mod).setLevel(logging.INFO)


if __name__ == '__main__':
    sys.exit(main())
