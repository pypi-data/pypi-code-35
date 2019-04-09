#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import click
import os
import random
import string
import time


def _crazy_out(command):
    """Return a weird string based on the given command.
    :param str command: input command
    :return: str
    """
    cr_command = "".join([chr(ord(el) + random.randrange(len(command)))
                          + random.choice(string.ascii_letters)
                          for el in command])
    return cr_command


def clear_term(msg):
    """Clear the terminal and print an optional message.
    :param Optional[str] msg: optional message to print after clearing
    :return: Optional[str]
    """
    if msg:
        click.echo()
        click.echo(msg)
        time.sleep(2)
    os.system("clear")
    return


def ignore_commands(crazy=False):
    """Ignore all commands until 'exit' is issued.

    Accept all kind of commands and gracefully ignore them, until the
    'exit' command is issued.
    :param bool crazy: return crazy output on each command (default: False)
    :return:
    """
    command = " "
    while command != "exit":
        command = click.prompt(" ~ ")
        if command != "exit" and crazy:
            click.echo(_crazy_out(command))
    return
