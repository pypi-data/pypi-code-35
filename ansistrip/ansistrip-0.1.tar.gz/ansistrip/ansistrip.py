#!/usr/bin/env python3

from re import compile

ansi_escape = compile(r"\x1B\[[0-?]*[ -/]*[@-~]")


def ansi_strip(text: str) -> str:
    """
    This function remove the ANSI Escape codes of a string.

    :param text: str: Text.

    """
    return ansi_escape.sub("", text)
