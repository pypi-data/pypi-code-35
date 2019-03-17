# -*- coding: utf-8 -*-
#
#   ktug-hanyang-pua: KTUG HanYang PUA conversion table reader
#   Copyright (C) 2015-2017 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from argparse import ArgumentParser
import gettext
import io
import logging
import os.path
import sys

# PYTHON_ARGCOMPLETE_OK
try:
    import argcomplete
except ImportError:
    argcomplete = None

from . import __version__
from .fileformats.table_binary import load_mappings_as_binary_table
from .fileformats.table_binary import dump_mappings_as_binary_table
from .fileformats.table_json import dump_mappings_as_json_table
from .fileformats.table_json import load_mappings_as_json_table
from .fileformats.table_text import load_mappings_as_text_table
from .fileformats.table_text import dump_mappings_as_text_table
from .fileformats.tree_binary import dump_tree_as_binary
from .fileformats.tree_json import dump_tree_as_json
from .models import Mapping
from .table import switch_source_and_targets
from .tree import build_tree

PY3 = sys.version_info.major == 3
logger = logging.getLogger(__name__)

locale_dir = os.path.join(os.path.dirname(__file__), 'locale')
t = gettext.translation('ktug-hanyang-pua', locale_dir, fallback=True)
if PY3:
    _ = t.gettext
else:
    _ = t.ugettext


def open_input(filename, format):
    if format == 'text':
        if filename is not None:
            if PY3:
                return io.open(filename, 'r', encoding='utf-8')
            else:
                # Note: parsec in Python 2 requires str
                return io.open(filename, 'rb')
        else:
            return sys.stdin
    if format == 'binary':
        if filename is not None:
            return io.open(filename, 'rb')
        else:
            if PY3:
                return sys.stdin.buffer
            else:
                return sys.stdin
    if format == 'json':
        if filename is not None:
            return io.open(filename, 'r', encoding='utf-8')
        else:
            return sys.stdin
    logger.error(
        _('Unsupported input format: %s', format)
    )
    raise SystemExit(1)


def open_output(filename, output_format):
    if output_format == 'text':
        if filename is not None:
            if PY3:
                return io.open(filename, 'w', encoding='utf-8')
            else:
                return io.open(filename, 'wb')
        else:
            return sys.stdout
    if output_format == 'binary':
        if filename is not None:
            return io.open(filename, 'wb')
        else:
            if PY3:
                return sys.stdout.buffer
            else:
                return sys.stdout
    if output_format == 'json':
        if filename is not None:
            if PY3:
                return io.open(filename, 'w', encoding='utf-8')
            else:
                return io.open(filename, 'wb')
        else:
            return sys.stdout
    logger.error(
        _('Unsupported output format: %s', output_format)
    )
    raise SystemExit(1)


def main():
    gettext.gettext = t.gettext
    parser = main_argparse()
    if argcomplete:
        argcomplete.autocomplete(parser)
    args = parser.parse_args()
    configureLogging(args.verbose)
    logger.info('args: %s', args)

    with open_input(args.INPUT_FILE, args.input_format) as input_fp:
        if args.input_format == 'text':
            parsed = load_mappings_as_text_table(input_fp)
        elif args.input_format == 'binary':
            parsed = load_mappings_as_binary_table(input_fp)
        elif args.input_format == 'json':
            parsed = load_mappings_as_json_table(input_fp)
        else:
            logger.error(
                _('Unsupported input format: %s', args.input_format)
            )
            raise SystemExit(1)

        with open_output(args.output_file, args.output_format) as output_fp:
            if args.data_model == 'table':
                if args.switch:
                    parsed = switch_source_and_targets(parsed)

                if args.output_format == 'binary':
                    if output_fp.isatty():
                        logger.error(
                            _('Rejecting to output binary to a terminal.')
                        )
                        raise SystemExit(1)
                    mappings = (
                        line for line in parsed
                        if isinstance(line, Mapping)
                    )
                    n_groups, n_mappings = dump_mappings_as_binary_table(
                        mappings,
                        output_fp
                    )
                    logger.info(
                        _('%s groups of %s mappings have been written.'),
                        n_groups,
                        n_mappings,
                    )
                elif args.output_format == 'json':
                    mappings = (
                        line for line in parsed
                        if isinstance(line, Mapping)
                    )
                    n_mappings = dump_mappings_as_json_table(
                        mappings, output_fp
                    )
                    logger.info(
                        _('%s mappings have been written.'), n_mappings,
                    )
                elif args.output_format == 'text':
                    n = dump_mappings_as_text_table(parsed, output_fp)
                    logger.info(
                        _('%s lines have been written.'), n
                    )
                else:
                    logger.error(
                        _('Not supported format for data model %s: %s'),
                        args.data_model,
                        args.output_format,
                    )
                    raise SystemExit(1)
            elif args.data_model == 'tree':
                mappings = (
                    line for line in parsed
                    if isinstance(line, Mapping)
                )
                # tree 모형은 사상 방향이 반대
                if not args.switch:
                    mappings = (
                        Mapping(
                            source=m.target,
                            target=m.source,
                            comment=m.comment
                        )
                        for m in mappings
                    )
                mappings = (
                    Mapping(
                        source=m.source,
                        target=m.target[0],
                        comment=m.comment,
                    )
                    for m in mappings
                )
                tree, __ = build_tree(mappings)

                if args.output_format == 'binary':
                    if output_fp.isatty():
                        logger.error(
                            _('Rejecting to output binary to a terminal.')
                        )
                        raise SystemExit(1)
                    n = dump_tree_as_binary(tree, output_fp)
                    logger.info(
                        _('%s nodes have been written.'), n
                    )
                elif args.output_format == 'json':
                    n_nodes = dump_tree_as_json(tree, output_fp)
                    logger.info(
                        _('%s nodes have been written.'), n_nodes,
                    )
                else:
                    logger.error(
                        _('Not supported format for data model %s: %s'),
                        args.data_model,
                        args.output_format,
                    )
                    raise SystemExit(1)


def main_argparse():
    parser = ArgumentParser()
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(__version__),
        help=_('output version information and exit')
    )
    parser.add_argument(
        '-v', '--verbose',
        action='count',
        help=_('increase verbosity')
    )
    parser.add_argument(
        '-o', '--output-file',
        action='store',
        help=_('Output file. The standard output will be used if ommitted.')
    )
    parser.add_argument(
        '-m', '--data-model',
        choices=('table', 'tree'),
        default='table',
        help=_(
            'Data model. Note that `table\' model is suitable for encoding '
            'and `tree\' model is suitable for decoding.'
        ),
    )
    parser.add_argument(
        '--input-format',
        action='store',
        choices=('text', 'binary', 'json'),
        default='text',
        help=_('Input format'),
    )
    parser.add_argument(
        '-F', '--output-format',
        action='store',
        choices=('text', 'binary', 'json'),
        default='text',
        help=_('Output format'),
    )
    parser.add_argument(
        '-S', '--switch',
        action='store_true',
        help=_('Switch source/targets in input mappings'),
    )
    parser.add_argument(
        'INPUT_FILE',
        action='store',
        nargs='?',
        default=None,
        help=_('Input file. The standard input will be used if ommitted.'),
    )
    return parser


def configureLogging(verbosity):
    verbosity = verbosity or 0
    if verbosity == 1:
        level = logging.INFO
    elif verbosity > 1:
        level = logging.DEBUG
    else:
        level = logging.WARNING
    try:
        import coloredlogs
    except ImportError:
        logging.basicConfig(level=level)
    else:
        coloredlogs.install(level)
