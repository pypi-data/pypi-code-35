#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import sys
import click
from .functions import ignore_commands, clear_term


@click.command()
@click.option("--crazy", "-c", is_flag=True, default=False,
              help="""Return crazy output on each command issued 
              (default: False)""")
@click.option("--silent", "-s", is_flag=True, default=False,
              help="""Drop all messages when starting and exiting 
              (default: False)""")
@click.version_option()
def main(crazy, silent):
    """Ignore every command until 'exit' is issued.
    """
    if silent:
        clear_term()
    else:
        clear_term("It's lunchtime!")
    ignore_commands(crazy=crazy)
    if silent:
        clear_term()
    else:
        clear_term("Lunchtime's over :(")

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
