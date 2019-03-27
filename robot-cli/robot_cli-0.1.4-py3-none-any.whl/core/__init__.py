import pkgutil
import sys

import os
from argparse import ArgumentParser
from importlib import import_module

from robot_cli.__version__ import __title__, __version__


class CommandError(Exception):
    """
    Exception class indicating a problem while executing a command.
    """

    def __init__(self, msg='', *args):
        self.msg = msg
        super(CommandError, self).__init__(*args)


def get_commands():
    command_dir = os.path.join(__path__[0], "commands")
    subcommands = [name for _, name, is_pkg in
                   pkgutil.iter_modules([command_dir])
                   if not is_pkg and not name.startswith("_")]
    subcommands.sort()
    return subcommands


def load_command_class(prog, subcommand, stdin=sys.stdin, stdout=sys.stdout,
                       stderr=sys.stderr):
    cmd_module = import_module("robot_cli.core.commands.%s" % subcommand)
    return cmd_module.Command(prog=prog, stdin=stdin, stdout=stdout,
                              stderr=stderr)


class ManagementUtility(object):
    def __init__(self, argv=None, stdin=sys.stdin, stdout=sys.stdout,
                 stderr=sys.stderr):
        self.argv = argv or sys.argv
        self.prog = __title__
        self.version = '%s %s' % (__title__, __version__)
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

    def main_help_text(self):
        """
        Returns the script's main help text, as a string.
        """
        usage = [
            "Type '%s help <subcommand>' for help on a specific subcommand." % self.prog,
            "",
            "Available subcommands:",
        ]
        for subcommand in get_commands():
            usage.append("  %s" % subcommand)
        usage.append("")

        return "\n".join(usage)

    def unknown_command_text(self, subcommand):
        text = [
            "Unknown command: %r" % subcommand,
            "Type '%s help' for usage." % self.prog,
            "",
        ]
        return "\n".join(text)

    def fetch_command(self, subcommand):
        subcommands = get_commands()
        if subcommand not in subcommands:
            self.stderr.write(self.unknown_command_text(subcommand))
            sys.exit(1)
        return load_command_class(self.prog, subcommand, stdin=self.stdin,
                                  stdout=self.stdout, stderr=self.stderr)

    def create_parser(self):
        parser = ArgumentParser(prog=self.prog, usage=self.main_help_text())
        parser.add_argument("-v", "--version")
        return parser

    def execute(self):
        subcommand = "help" if len(self.argv) <= 1 else self.argv[1].lower()
        if subcommand == "help":
            if len(self.argv) < 3:
                self.create_parser().print_help()
            else:
                self.fetch_command(self.argv[2]).print_help()
        elif subcommand in ("-h", "--help"):
            self.create_parser().print_help()
        elif subcommand in ("-v", "--version", "version"):
            self.stdout.write(self.version + "\n")
        else:
            self.fetch_command(subcommand).run_from_argv(self.argv)


def execute_from_command_line(argv=None):
    utility = ManagementUtility(argv)
    utility.execute()
