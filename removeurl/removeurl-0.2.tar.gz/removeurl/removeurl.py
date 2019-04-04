#!/usr/bin/env python3

from re import sub, MULTILINE


def remove_url(text: str) -> str:
    """
    Remove URLs from text if they start with http or https.

    :param text: str: Text to sanitize.

    """
    return sub(
        r"https?:\/\/.*[\b\r\n]*",
        "",
        text, flags=MULTILINE
        )
