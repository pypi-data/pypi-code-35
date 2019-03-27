from argparse import ArgumentParser

import sys

from robot_cli.core import CommandError
from robot_cli.__version__ import __title__


class BaseCommand(object):
    def __init__(self, prog=__title__, stdin=sys.stdin, stdout=sys.stdout,
                 stderr=sys.stderr):
        self.prog = prog
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

    @property
    def command(self):
        return self.__module__.split(".")[-1]

    @property
    def description(self):
        return ""

    def create_parser(self):
        """
        Create and return the ``ArgumentParser`` which will be used to
        parse the arguments to this command.
        """
        prog = "%s %s" % (self.prog, self.command)
        parser = ArgumentParser(prog=prog, description=self.description)
        self.add_arguments(parser)
        return parser

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        :type parser: argparse.ArgumentParser
        """
        pass

    def print_help(self):
        """
        Print the help message for this command, derived from ``self.usage()``.
        """
        parser = self.create_parser()
        parser.print_help()

    def run_from_argv(self, argv):
        parser = self.create_parser()

        opts, args = parser.parse_known_args(argv[2:])
        cmd_opts = vars(opts)
        try:
            self.execute(*args, **cmd_opts)
        except Exception as e:
            if not isinstance(e, CommandError):
                raise e
            self.stderr.write(e.msg + "\n")
            sys.exit(1)

    def execute(self, *args, **options):
        """
        Try to execute this command.
        """
        output = self.handle(*args, **options)
        if output:
            self.stdout.write(output)

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        raise NotImplementedError(
            "subclasses of BaseCommand must provide a handle() method")
