# -*- coding: utf-8 -*-

from textwrap import dedent
import sys

import termcolor


class FormatterMessage(object):

    def __init__(self, submodule):
        print(f'{submodule}')
        self.doc_migration = self.indent(submodule.header(), 4)
        self.doc_up = self.indent(submodule.doc_up(), 4).strip()
        self.doc_down = self.indent(submodule.doc_down(), 4).strip()
        self.version_migrate = f'{submodule.version}'
        self.archive_name = submodule.filename()
        self.execute = submodule.execute
        self.term_color = "white" if self.execute else "yellow"

    def message(self, method):
        top_line = termcolor.colored(
            f'{self.version_migrate} - {self.archive_name} -- Dry Run: {not self.execute}',
            self.term_color
        )
        output = (
            f'\n{termcolor.colored(method.upper() + ":", "red")} '
            f'{top_line}\n'
            f'{termcolor.colored(self.doc_migration, "blue")}\n\n'
            f'{self.indent("- " + termcolor.colored(self.doc_up if method == "upgrade" else self.doc_down, self.term_color), 8)}\n'
        )

        return output

    @staticmethod
    def print_message(body, color='white'):
        return (
            f'{FormatterMessage.indent(termcolor.colored("- Output", "white"), 8)}\n'
            f'{FormatterMessage.indent(termcolor.colored(body, color), 12)}\n-----\n'
        )

    @staticmethod
    def indent(text, space=18):
        text = dedent(text)
        lines = text.split("\n")
        text_ident = " "*space
        text = text_ident + ("\n" + text_ident).join(lines)
        return text

    def message_error(self, method, error):
        message_error = f'{termcolor.colored(error, "red")}'
        return message_error


class TerminalMessages(object):

    def __init__(self, migrations, **kwargs):
        self.migrations = migrations
        print("Running command: link_migration %s" % " ".join(sys.argv[1:]), flush=True)

    def current_version(self):
        print(self.migrations.current_version, flush=True)

    def make_message(self, method=None, migration=None):
        print(FormatterMessage(migration).message(method=method), flush=True)

    def print_message(self, message=None, color=None):
        print(FormatterMessage.print_message(body=message, color=color), flush=True)

    def error_message(self, method, migration, error):
        print(FormatterMessage(migration).message_error(method, error), flush=True)
