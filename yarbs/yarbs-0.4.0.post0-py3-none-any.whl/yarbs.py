#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=superfluous-parens


from logging import getLogger as _getLogger
_logger = _getLogger('yarbs')  # pylint: disable=invalid-name


DEFAULT_BACKUPS_KEPT = 30
DEFAULT_RSYNC_COMMAND = 'rsync'
DEFAULT_VERBOSE = False
DEFAULT_COMPRESSION = False
DEFAULT_BWLIMIT = -1
DEFAULT_SSH_SERVER = None

# Date component ranges are ignored. Seconds also might not be needed to be used.
TIMESTAMP_PATTERN = r'\d{4}-\d{2}-\d{2}T\d{2}-\d{2}(?:-\d{2})?'
TEMPORARY_SUFFIX = '.tmp'


def _get_backup_basename(source_dir):
    """
    Get the base name used to name destination directories.
    """

    from os.path import basename, dirname

    name = basename(source_dir)  # If specified as "some/path".
    if (not name):  # If specified as "some/path/".
        name = basename(dirname(source_dir))
    return name


def _get_backup_name(basename):
    """
    Create a name for a current backup, including timestamp suffix.
    """

    from datetime import datetime

    return "{}_{}".format(
        basename,
        datetime.now().replace(microsecond=0).isoformat().replace(':', '-'))


def _is_matching_backup_name(name, basename, unfinished=False):
    """
    Check if an item is a backup of a specified base name.
    """

    from re import match, escape

    pattern = "^{}_{}{}$".format(
        escape(basename),
        TIMESTAMP_PATTERN,
        escape(TEMPORARY_SUFFIX) if (unfinished) else '')
    return (match(pattern, name) is not None)


def _list_existing_backups(destination_dir, backup_basename):
    """
    List the paths of the existing backups in the destination directory.
    """

    from os import listdir
    from os.path import join, isdir

    backup_paths = []
    unfinished_backup_paths = []
    for item_name in listdir(destination_dir):
        item_path = join(destination_dir, item_name)
        if (isdir(item_path)):
            if (_is_matching_backup_name(item_name, backup_basename)):
                backup_paths.append(item_path)
            elif (_is_matching_backup_name(item_name, backup_basename, unfinished=True)):
                unfinished_backup_paths.append(item_path)
    return (sorted(backup_paths), sorted(unfinished_backup_paths))


def _remove_unfinished_backups(backups):
    from shutil import rmtree

    for backup_path in backups:
        _logger.info("Removing unfinished backup: %s", backup_path)
        rmtree(backup_path)


def _remove_old_backups(existing_backups, backups_kept):
    """
    Remove old backups above the limit plus one more to make space for
    a new backup.
    """

    from shutil import rmtree

    while (len(existing_backups) >= backups_kept):
        backup_path = existing_backups.pop(0)
        _logger.info("Removing old backup: %s", backup_path)
        rmtree(backup_path)


def _get_backup_path(destination_dir, backup_name):
    """
    Get a path to the specific backup.
    """

    from os.path import join

    return join(destination_dir, backup_name)


def _normalize_dir_path(path):
    """
    Normalize directory path to include separator ("/") at the end.
    """

    from os import sep

    if (path[-1] not in ['/', '\\']):
        path += sep
    return path


def _move(source, destination, ssh_server=None):
    """
    "mv" source to destination, optionally via SSH.
    """

    from os import rename
    from subprocess import check_call

    if (ssh_server is None):
        rename(source, destination)
    else:
        check_call(['ssh', ssh_server, 'mv', source, destination])


def _rmtree(target, ssh_server=None):
    """
    "rm -r" target, optionally via SSH.
    """

    from shutil import rmtree
    from subprocess import check_call

    if (ssh_server is None):
        rmtree(target)
    else:
        check_call(['ssh', ssh_server, 'rm', '-r', target])


def _create_backup(
        source_dir, backup_path, previous_backup_path,
        verbose=DEFAULT_VERBOSE, rsync_command=DEFAULT_RSYNC_COMMAND,
        compression=DEFAULT_COMPRESSION, bwlimit=DEFAULT_BWLIMIT):
    """
    Create a source directory backup to the specified path, optionally
    linking to a previous backup.
    """

    from subprocess import check_call
    from os.path import abspath

    switches = ['-i', '-a', '--delete']
    if (verbose):
        switches.append('-v')
    if (compression):
        switches.append('-z')
    if (bwlimit > 0):
        switches.append("--bwlimit={}".format(bwlimit))
    if (previous_backup_path is not None):
        previous_backup_path = _normalize_dir_path(abspath(previous_backup_path))
        switches.append("--link-dest={}".format(previous_backup_path))

    source_dir = _normalize_dir_path(source_dir)
    backup_path = _normalize_dir_path(backup_path)
    check_call([rsync_command] + switches + [source_dir, backup_path])


def _check_if_root():
    """
    Check if running as root (required by some rsync settings).
    """

    from subprocess import check_output

    user = check_output('whoami').decode().strip()
    if (user != 'root'):
        _logger.info('Not running as root. Source permissions won\'t be kept.')


def prepare(
        source_dir, destination_dir,
        backups_kept=DEFAULT_BACKUPS_KEPT):
    """
    Prepare for an incremental backup.

    Lists existing backups and performs a cleanup to make space for a
    new backup.

    source_dir -- Path to the backed-up directory.
    destination_dir -- Path to the directory containing backups.
    backups_kept -- Maximum number of backups to be kept.

    Returns -- A (backup_path, previous_backup_path) tuple, where:
        backup_path -- Absolute path to the backup directory to be
            created.
        previous_backup_path -- Absolute path to the last backup to be
            used as hardlink source or None if no backup yet exists.
    """

    from os.path import exists, abspath

    if (not exists(destination_dir)):
        raise AttributeError('Destination directory does not exist.')
    if (backups_kept < 1):
        raise AttributeError('Must keep at least one backup.')

    backup_basename = _get_backup_basename(source_dir)
    _logger.info("Preparing \"%s\" backup.", backup_basename)
    _logger.debug("Source dir: %s", source_dir)
    _logger.debug("Destination dir: %s", destination_dir)

    existing_backups, unfinished_backups = _list_existing_backups(
        destination_dir, backup_basename)
    _logger.debug(
        "Found %d existing backup(s) and %d unfinished.",
        len(existing_backups), len(unfinished_backups))
    _remove_unfinished_backups(unfinished_backups)
    _remove_old_backups(existing_backups, backups_kept)

    backup_name = _get_backup_name(backup_basename)
    backup_path = _get_backup_path(destination_dir, backup_name)
    _logger.info("Backup dir: %s", backup_path)
    return (
        abspath(backup_path),
        abspath(existing_backups[-1]) if (existing_backups) else None)


def sync(
        source_dir, backup_path, previous_backup_path,
        rsync_command=DEFAULT_RSYNC_COMMAND, verbose=DEFAULT_VERBOSE,
        compression=DEFAULT_COMPRESSION, bwlimit=DEFAULT_BWLIMIT,
        ssh_server=DEFAULT_SSH_SERVER):
    """
    Perform a backup.

    Last backup made is used as a target for unchanged files to link to.
    This avoids both copying the unchanged files and saves space in the
    destination directory.

    The syncing uses -a and --delete rsync arguments. See "man rsync"
    for more details.

    Needs to be ran as root (e.g. with "sudo").

    source_dir -- Path to the backed-up directory.
    backup_path -- Path to the backup directory to be created.
    previous_backup_path -- Path to the last backup to be
        used as hardlink source or None if no backup yet exists.
    rsync_command -- Custom rsync executable path.
    verbose -- Enables higher rsync verbosity.
    compression -- Enables rsync transport compression.
    bwlimit -- Limit socket I/O bandwidth [kbps]. -1 for unlimited.
    ssh_server -- SSH user@hostname or config used for backup
        destination.
    """

    from os.path import exists
    from shutil import rmtree

    _check_if_root()
    if (not exists(source_dir)):
        raise AttributeError('Source directory does not exist.')

    backup_basename = _get_backup_basename(source_dir)
    _logger.info("Syncing \"%s\" backup.", backup_basename)

    temporary_backup_path = backup_path + TEMPORARY_SUFFIX
    try:
        rsync_backup_path = (
            temporary_backup_path
            if (ssh_server is None) else
            "{}:{}".format(ssh_server, temporary_backup_path))
        _create_backup(
            source_dir, rsync_backup_path,
            previous_backup_path,
            rsync_command=rsync_command, verbose=verbose,
            compression=compression, bwlimit=bwlimit)
    except:
        _logger.error(
            # pylint: disable=W1201
            'An error was encountered or the process was interrupted. ' +
            'The unfinished backup will be removed...')
        _rmtree(temporary_backup_path, ssh_server=ssh_server)
        raise
    _move(temporary_backup_path, backup_path, ssh_server=ssh_server)
    _logger.info("Finished \"%s\" backup.", backup_basename)


def backup(
        source_dir, destination_dir,
        backups_kept=DEFAULT_BACKUPS_KEPT,
        rsync_command=DEFAULT_RSYNC_COMMAND,
        verbose=DEFAULT_VERBOSE,
        compression=DEFAULT_COMPRESSION,
        bwlimit=DEFAULT_BWLIMIT):
    """
    Create an incremental backup of a source directory to a new
    directory created under destination directory.

    Existing backups in the destination directory that are above the
    limit of backup to be kept are removed. Last backup made is used
    as a target for unchanged files to link to. This avoids both copying
    the unchanged files and saves space in the destination directory.

    The syncing uses -a and --delete rsync arguments. See "man rsync"
    for more details.

    Needs to be ran as root (e.g. with "sudo").

    source_dir -- Path to the backed-up directory.
    destination_dir -- Path to the directory containing backups.
    backups_kept -- Maximum number of backups to be kept.
    rsync_command -- Custom rsync executable path.
    verbose -- Enables higher rsync verbosity.
    compression -- Enables rsync transport compression.
    bwlimit -- Limit socket I/O bandwidth [kbps]. -1 for unlimited.
    """

    # TODO: Could work over SSH on its own.
    backup_path, previous_backup_path = prepare(
        source_dir, destination_dir, backups_kept=backups_kept)
    sync(
        source_dir, backup_path, previous_backup_path,
        rsync_command=rsync_command, verbose=verbose,
        compression=compression, bwlimit=bwlimit)


def _setup_logging(verbose=False):
    from logging import basicConfig, INFO, DEBUG

    basicConfig(
        level=(INFO if (not verbose) else DEBUG),
        format='%(levelname)-5s: %(message)s')


def _print_backup_dirs(backup_path, previous_backup_path):
    from json import dumps

    print(dumps({
        'backup_path': backup_path,
        'previous_backup_path': previous_backup_path,
        }))


def _read_backup_dirs():
    from json import load
    from sys import stdin

    backup_dirs = load(stdin)
    return (backup_dirs['backup_path'], backup_dirs['previous_backup_path'])


SOURCE_DIR_DESCRIPTION = 'Path or name of the backed-up directory.'
DESTINATION_DIR_DESCRIPTION = 'Path to the directory containing backups.'
BACKUPS_KEPT_DESCRIPTION = 'Maximum number of backups to be kept.'
RSYNC_COMMAND_DESCRIPTION = 'Custom rsync executable path.'
COMPRESSION_DESCRIPTION = 'Apply compression.'
BWLIMIT_DESCRIPTION = 'Limit socket I/O bandwidth [kbps]. -1 for unlimited.'


def _parse_args(args=None):
    from argparse import ArgumentParser
    from . import __version__

    parser = ArgumentParser(
        description='Create incremental backups using Rsync.')
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose mode.')
    parser.add_argument(
        '--version',
        action='version',
        version=__version__)

    subparsers = parser.add_subparsers(
        help='Performed action (typically "backup").',
        dest='action')

    backup_parser = subparsers.add_parser(
        'backup',
        help=(
            'Make space, find the latest backup and create a new ' +
            'backup.'))
    backup_parser.add_argument(
        'source_dir',
        help=SOURCE_DIR_DESCRIPTION)
    backup_parser.add_argument(
        'destination_dir',
        help=DESTINATION_DIR_DESCRIPTION)
    backup_parser.add_argument(
        '--backups-kept',
        type=int,
        default=DEFAULT_BACKUPS_KEPT,
        help=BACKUPS_KEPT_DESCRIPTION)
    backup_parser.add_argument(
        '--rsync-command',
        default=DEFAULT_RSYNC_COMMAND,
        help=RSYNC_COMMAND_DESCRIPTION)
    backup_parser.add_argument(
        '-c', '--compression',
        action='store_true',
        help=COMPRESSION_DESCRIPTION)
    backup_parser.add_argument(
        '--bwlimit',
        type=int,
        default=DEFAULT_BWLIMIT,
        help=BWLIMIT_DESCRIPTION)

    prepare_parser = subparsers.add_parser(
        'prepare',
        help=(
            'Make space, find the latest backup and print the paths ' +
            'to stdout as JSON.'))
    prepare_parser.add_argument(
        'source_dir',
        help=SOURCE_DIR_DESCRIPTION)
    prepare_parser.add_argument(
        'destination_dir',
        help=DESTINATION_DIR_DESCRIPTION)
    prepare_parser.add_argument(
        '--backups-kept',
        type=int,
        default=DEFAULT_BACKUPS_KEPT,
        help=BACKUPS_KEPT_DESCRIPTION)

    sync_parser = subparsers.add_parser(
        'sync',
        help=(
            'Create a new backup using the provided paths to ' +
            'previous and new backup dirs.'))
    sync_parser.add_argument(
        'source_dir',
        help=SOURCE_DIR_DESCRIPTION)
    sync_parser.add_argument(
        'backup_path',
        type=str,
        nargs='?',
        help=(
            'Specific path of the new backup directory (read as JSON ' +
            'from stdin if unspecified).'))
    sync_parser.add_argument(
        'previous_backup_path',
        type=str,
        nargs='?',
        help=(
            'Specific path of the latest previous backup directory ' +
            '(read as JSON from stdin if unspecified).'))
    sync_parser.add_argument(
        '--rsync-command',
        default=DEFAULT_RSYNC_COMMAND,
        help=RSYNC_COMMAND_DESCRIPTION)
    sync_parser.add_argument(
        '-c', '--compression',
        action='store_true',
        help=COMPRESSION_DESCRIPTION)
    sync_parser.add_argument(
        '--bwlimit',
        type=int,
        default=DEFAULT_BWLIMIT,
        help=BWLIMIT_DESCRIPTION)
    sync_parser.add_argument(
        '--ssh-server',
        type=str,
        default=DEFAULT_SSH_SERVER,
        help='SSH user@hostname or config used for backup destination.')

    return parser.parse_args(args)


def main(args=None):
    config = _parse_args(args)
    _setup_logging(config.verbose)
    if (config.action == 'backup'):
        backup(
            config.source_dir,
            config.destination_dir,
            backups_kept=config.backups_kept,
            rsync_command=config.rsync_command,
            verbose=config.verbose,
            compression=config.compression,
            bwlimit=config.bwlimit)
    elif (config.action == 'prepare'):
        _print_backup_dirs(*prepare(
            config.source_dir,
            config.destination_dir,
            backups_kept=config.backups_kept))
    elif (config.action == 'sync'):
        backup_path = config.backup_path
        previous_backup_path = config.previous_backup_path
        if (backup_path is None or
                previous_backup_path is None):
            backup_path, previous_backup_path = _read_backup_dirs()
        sync(
            config.source_dir,
            backup_path,
            previous_backup_path,
            rsync_command=config.rsync_command,
            verbose=config.verbose,
            compression=config.compression,
            bwlimit=config.bwlimit,
            ssh_server=config.ssh_server)
    else:
        raise ValueError('Bad action. See --help.')


if (__name__ == '__main__'):
    main()
