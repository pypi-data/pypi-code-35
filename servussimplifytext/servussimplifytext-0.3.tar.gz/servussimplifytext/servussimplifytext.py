#!/usr/bin/env python3

from re import sub


def simplify_text_no_symbols(text: str) -> str:
    """
    Simplify text just filtering for a subset of ASCII characters and symbols.

    :param text: str: Text to be cleaned.

    """
    return " ".join(
        sub(
            r"([^0-9A-Za-z \t])",
            " ",
            text
            ).split()
        )


def simplify_text(text: str) -> str:
    """
    Simplify text filtering for a subset of ASCII characters.

    :param text: str: Text to be cleaned.

    """
    return " ".join(
        sub(
            r"([^0-9A-Za-z \t\¿\?\.\,\:\;]\(\)\[\]\{\}\!\¡)"
            r"\*\+\-\/\\\"\#\$\%\&\=",
            " ",
            text
            ).split()
        )
