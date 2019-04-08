#! /usr/bin/env python
from __future__ import print_function

import sys

from .termcolors import green, red, yellow

QUESTION_MARK = u"\u2753"
CHECK_MARK = u"\u2713"
BALLOT_X = u"\u2717"
RIGHT_BACKWARDS_ARROW = u"\u27a1"
RAISED_HAND = u"\u270B"


def term_print(string, **kwds):
    try:
        print(string, **kwds)
    except UnicodeEncodeError:
        print(string.encode("utf-8"), **kwds)


def prompt(msg, default=None, batch_mode=False):
    if not isinstance(default, (type(None), bool)):
        raise ValueError("default not bool or None")

    if batch_mode:
        return default is None or default

    msg += " (y or n)? "
    if default is not None:
        msg += (default and "[y] ") or "[n] "
    msg = green(msg)

    resp = None
    while not isinstance(resp, bool):
        term_print(green(RAISED_HAND), end=" ")
        resp = input(msg) or default
        if resp in ("y", "n"):
            resp = resp == "y"

    return resp


def status(message):
    """Print a status message.

    Parameters
    ----------
    message : str
        The message to display.

    """
    term_print(yellow(" ".join([RIGHT_BACKWARDS_ARROW, message])), file=sys.stderr)


def success(message):
    """Print a success message.

    Parameters
    ----------
    message : str
        The message to display.

    """
    term_print(green(" ".join([CHECK_MARK, message])), file=sys.stderr)


def error(message):
    """Print an error message.

    Parameters
    ----------
    message : str
        The message to display.

    """
    term_print(red(" ".join([BALLOT_X, message])), file=sys.stderr)
