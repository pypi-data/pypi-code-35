import argparse
import textwrap

from .base import RegisteredCommandBase, RegisteredSubCommandBase
from ..parsers import object_id_parser


###############################################################################
# Base command
###############################################################################
registry = []
class DeleteCommand(RegisteredCommandBase):
    name = "delete"
    description = "Delete a superevent signoff"
    subcommands = registry


###############################################################################
# Subcommands - registered to base command automatically
###############################################################################
class DeleteChildBase(RegisteredSubCommandBase):
    _registry = registry


class DeleteSignoffCommand(DeleteChildBase):
    name = "signoff"
    description = "Delete a superevent signoff"
    long_description = textwrap.dedent("""\
        Delete an operator or advocate signoff. Only allowed for superevents;
        event signoff deletion is not presently implemented.
    """).rstrip()
    parent_parsers = (object_id_parser,)

    def add_custom_arguments(self, parser):
        parser.add_argument("signoff_type", type=str,
            help=("Signoff type (do '{prog} show signoff_types') to see "
            "options").format(prog=self.base_prog))
        parser.add_argument("instrument", type=str, nargs='?',
            help=("Instrument code (do {prog} show instruments to see "
            "options). Required for operator signoffs.").format(
            prog=self.base_prog))
        return parser

    def run(self, client, args):
        instrument = args.instrument or '' # Convert None to ''
        return client.delete_signoff(args.object_id, args.signoff_type,
            instrument=instrument)
