#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
msbackup -- Generic archive utility.

@author:     Aleksei Badiaev <aleksei.badyaev@gmail.com>
@copyright:  2015 Aleksei Badiaev. All rights reserved.
"""

import os
import sys
import traceback
import argparse
import configparser

from msbackup.archive import ARCHIVERS
from msbackup.encrypt import ENCRYPTORS
from msbackup import backend


__all__ = ('main', )
__date__ = '2015-10-08'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

UPDATE_DATE = __date__
with open(os.path.join(PROJECT_ROOT, 'UPDATE_DATE')) as update_date_file:
    UPDATE_DATE = update_date_file.read().rstrip()
__updated__ = UPDATE_DATE

VERSION = 'UNKNOWN'
with open(os.path.join(PROJECT_ROOT, 'VERSION')) as version_file:
    VERSION = version_file.read().rstrip()
__version__ = VERSION

DEBUG = False


def main(argv=None):
    """
    Entry point in application.

    :param argv: Command line arguments.
    :type argv: list
    :return: Exit code of application.
    :rtype: int
    """
    global DEBUG
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)
    program_name = os.path.basename(sys.argv[0])
    program_version = 'v%s' % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version,
                                                     program_build_date)
    program_shortdesc = __import__('msbackup').msbackup.__doc__.split('\n')[1]
    program_license = """%s

  Created by Aleksei Badiaev <aleksei.badyaev@gmail.com> on %s.
  Copyright 2015 Aleksei Badiaev. All rights reserved.

  Distributed on an 'AS IS' basis without warranties
  or conditions of any kind, either express or implied.
""" % (program_shortdesc, str(__date__))

    try:
        archivers = sorted([item for item in ARCHIVERS])
        encryptors = sorted([item for item in ENCRYPTORS])
        # Setup argument parser
        parser = argparse.ArgumentParser(
            prog=program_name,
            description=program_license,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        parser.add_argument(
            '-c', '--config', metavar='FILE',
            help='Path to config file.',
        )
        parser.add_argument(
            '-b', '--backup-dir', dest='backup_dir',
            help='Path to archive directory (current by default).',
        )
        parser.add_argument(
            '-t', '--tmp-dir',
            help='Folder path for temporary files.'
        )
        parser.add_argument(
            '-a', '--archiver', choices=archivers,
            help='Name of file archiver.',
        )
        parser.add_argument(
            '-E', '--encryptor', choices=encryptors,
            help='Name of file encryptor.',
        )
        parser.add_argument(
            '-x', '--exclude', action='append', metavar='PATTERN',
            help='Exclude files defined by the PATTERN.',
        )
        parser.add_argument(
            '-X', '--exclude-from', dest='exclude_from',
            action='append', metavar='FILE',
            help='Exclude files defined in FILE.',
        )
        parser.add_argument(
            '-r', '--rotate', type=int,
            help='Number of archive files to be rotated.',
        )
        parser.add_argument(
            '-v', '--verbose', action='store_true',
            help='Verbose output.',
        )
        parser.add_argument(
            '-d', '--debug', action='store_true',
            help='Print traceback when errors occured.',
        )
        parser.add_argument(
            '-V', '--version', action='version',
            version=program_version_message,
        )

        # Парсеры различных режимов работы архиватора.

        def _get_param(params, kwargs, name):
            """Извлечение параметра из объекта."""
            value = getattr(params, name)
            if value is not None:
                kwargs[name] = value

        def _get_common_backend_kwargs(params):
            """Извлечение общих параметров конструктора движка."""
            kwargs = {}
            _get_param(params, kwargs, 'backup_dir')
            _get_param(params, kwargs, 'tmp_dir')
            _get_param(params, kwargs, 'rotate')
            _get_param(params, kwargs, 'archiver')
            _get_param(params, kwargs, 'encryptor')
            _get_param(params, kwargs, 'exclude')
            _get_param(params, kwargs, 'exclude_from')
            return kwargs

        def _get_file_backend_kwargs(params):
            """Подготовка параметров архиватора для режима 'file'."""
            kwargs = _get_common_backend_kwargs(params)
            _get_param(params, kwargs, 'archive_name')
            _get_param(params, kwargs, 'base_dir')
            return kwargs

        def _get_hg_backend_kwargs(params):
            """Подготовка параметров для режима 'hg'."""
            kwargs = _get_common_backend_kwargs(params)
            _get_param(params, kwargs, 'repos_dir')
            _get_param(params, kwargs, 'hg_cmd')
            return kwargs

        def _get_svn_backend_kwargs(params):
            """Подготовка параметров для режима 'svn'."""
            kwargs = _get_common_backend_kwargs(params)
            _get_param(params, kwargs, 'repos_dir')
            return kwargs

        def _get_pg_backend_kwargs(params):
            """Подготовка параметров для режима 'pg'."""
            kwargs = _get_common_backend_kwargs(params)
            _get_param(params, kwargs, 'host')
            _get_param(params, kwargs, 'port')
            _get_param(params, kwargs, 'username')
            return kwargs

        def _get_sqlite_backend_kwargs(params):
            """Подготовка параметров для режима 'sqlite'."""
            kwargs = _get_common_backend_kwargs(params)
            _get_param(params, kwargs, 'sqlite_cmd')
            _get_param(params, kwargs, 'compress_level')
            return kwargs

        def get_backup_kwargs(params):
            """Подготовка общих параметров архиватора."""
            return {
                'sources': params.source,
                'verbose': params.verbose,
            }

        subparsers = parser.add_subparsers(
            dest='backend',
            title='Back-end name',
        )
        # file
        parser_file = subparsers.add_parser('file')
        parser_file.set_defaults(get_backend_kwargs=_get_file_backend_kwargs)
        parser_file.add_argument(
            '-n', '--name', dest='archive_name', metavar='NAME',
            help='Name of archive file without extension.',
        )
        parser_file.add_argument(
            '-C', '--base-dir', dest='base_dir', metavar='DIR',
            help='Archiver will change to directory DIR.',
        )
        parser_file.add_argument(
            'source', nargs='*', metavar='PATH',
            help='Path to file or directory.')
        # hg
        parser_hg = subparsers.add_parser('hg')
        parser_hg.set_defaults(get_backend_kwargs=_get_hg_backend_kwargs)
        parser_hg.add_argument(
            '-R', '--repos-dir', dest='repos_dir',
            help='Path to root of Mercurial repositories.')
        parser_hg.add_argument(
            '--hg-cmd', dest='hg_cmd', help='Command to run mercurial util.')
        parser_hg.add_argument(
            'source', nargs='*', metavar='REPO',
            help='Name of repository.')
        # svn
        parser_svn = subparsers.add_parser('svn')
        parser_svn.set_defaults(get_backend_kwargs=_get_svn_backend_kwargs)
        parser_svn.add_argument(
            '-R', '--repos-dir', dest='repos_dir',
            help='Path to root of Subversion repositories.')
        parser_svn.add_argument(
            'source', nargs='*', metavar='REPO',
            help='Name of repository.')
        # pg
        parser_pg = subparsers.add_parser('pg')
        parser_pg.set_defaults(get_backend_kwargs=_get_pg_backend_kwargs)
        parser_pg.add_argument(
            'source', nargs='*', metavar='DBNAME', help='Name of database.')
        parser_pg.add_argument('-H', '--host', help='PostgreSQL hostname.')
        parser_pg.add_argument('-p', '--port', help='PostgreSQL port number.')
        parser_pg.add_argument('-U', '--username', help='PostgreSQL username.')
        # sqlite
        parser_sqlite = subparsers.add_parser('sqlite')
        parser_sqlite.set_defaults(
            get_backend_kwargs=_get_sqlite_backend_kwargs)
        parser_sqlite.add_argument(
            'source', nargs='*', metavar='DBNAME',
            help='Path to database file.')
        parser_sqlite.add_argument(
            '--sqlite-cmd',
            dest='sqlite_cmd',
            help='Command to run SQLite command-line shell.',
        )
        parser_sqlite.add_argument(
            '-z', '--compress-level',
            dest='compress_level', metavar='N',
            help='Set compression level to N for the compression algorithms.',
        )
        # -- Load configuration --
        params = parser.parse_args()
        config = configparser.RawConfigParser()
        if params.config is not None:
            config_file_path = params.config
            if not os.path.isfile(config_file_path):
                raise FileNotFoundError(config_file_path)
            config.read(config_file_path)
            setattr(config, 'config_file_path', config_file_path)
        if params.backend is None:
            parser.error(
                'the following arguments are required: Back-end')
        DEBUG = params.debug
        # Perform backup.
        back = backend.make_backend(
            name=params.backend,
            config=config,
            **params.get_backend_kwargs(params),
        )
        back.backup(**get_backup_kwargs(params))
        return 0
    except KeyboardInterrupt:  # pragma: no coverage
        return 0
    except Exception as e:
        indent = len(program_name) * ' '
        sys.stderr.write(program_name + ': ' + repr(e) + '\n')
        sys.stderr.write(indent + '  for help use --help\n')
        if DEBUG:  # pragma: no coverage
            traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no coverage
    sys.exit(main())
