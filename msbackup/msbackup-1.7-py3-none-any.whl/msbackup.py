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

from msbackup import backend
from msbackup.backend_base import Base as BaseBackend


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
    Точка входа в приложение.

    :param argv: Аргументы командной строки.
    :type argv: list
    :return: Код завершения приложения.
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
        parser = argparse.ArgumentParser(
            prog=program_name,
            description=program_license,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        subparsers = BaseBackend.make_options(
            parser=parser,
            version=program_version_message,
        )
        for backend_name in backend.INIT_BACKENDS_LIST:
            backend.BACKENDS[backend_name].make_subparser(subparsers)
        params = parser.parse_args()
        config = configparser.RawConfigParser()
        if params.config is not None:
            config_file_path = params.config
            if not os.path.isfile(config_file_path):
                raise FileNotFoundError(config_file_path)
            config.read(config_file_path)
            setattr(config, 'config_file_path', config_file_path)
        BaseBackend.validate_params(parser, params)
        DEBUG = params.debug
        # Perform backup.
        return backend.make_backend(
            name=params.backend,
            config=config,
            **params.get_backend_kwargs(params),
        ).backup(sources=params.source, verbose=params.verbose)
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
