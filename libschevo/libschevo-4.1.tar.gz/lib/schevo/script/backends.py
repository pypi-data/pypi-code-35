"""Installed backends command."""

# Copyright (c) 2001-2009 ElevenCraft Inc.
# See LICENSE for details.

from textwrap import dedent

from schevo.script.command import Command
from schevo.script import opt

usage = """\
schevo backends

Shows a list of installed backends and the options that each one
accepts."""


def _parser():
    p = opt.parser(usage)
    return p


class Backends(Command):

    name = 'Installed Backends'
    description = 'Show a list of installed backends.'

    def main(self, arg0, args):
        from schevo.backend import backends
        print (backends.__dict__)

start = Backends
