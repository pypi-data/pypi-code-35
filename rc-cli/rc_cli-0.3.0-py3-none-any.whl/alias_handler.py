import click
import sys
from .error_catcher.error_catcher import ErrorCatcher

class AliasHandler(click.Group):

    def get_command(self, ctx, cmd_name):
        """
        Bit confusing in the docs. To sum it up,
        1. Ask click if it has already matched with a command `cmd_name`.
            a. If so, forward the results.
            b. Check if it is an alias.

        This alias dictionary created must be correct. The value must
        match to an entry in `self.list_command` (i.e. things marked with
        `@cli.command`). If it returns None, click will handle the error.

        :param ctx: Click context
        :param cmd_name: Name of command being executed
        :return: command_name to execute
        """
        error_catcher = ErrorCatcher()
        sys.excepthook = error_catcher.catch_exception
        error_catcher.set_command(cmd_name)
        error_catcher.set_command_long(sys.argv)

        command = click.Group.get_command(self, ctx, cmd_name)
        if command is not None:
            return command

        aliases = {
            'cp': 'copy',
            'rm': 'remove'
        }

        alias_match = aliases.get(cmd_name, None)
        if alias_match is None:
            return None
        return click.Group.get_command(self, ctx, alias_match)
