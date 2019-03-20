#!/usr/bin/env python3

"""
Little Python3 module to simply check if text contains valid date or hour.
"""

from pendulum import from_format

from normalisedates import normalise_date

from typing import Optional, Tuple


def is_complete_hour(text: str, tz: str = "local") -> Optional[bool]:
    """
    Check if text is a valid hour.

    :param text: str: Text to check.
    :param tz: str:  (Default value = "local")

    """
    for fmt in ["HH:mm:ss", "HH:mm"]:
        try:
            from_format(text, fmt, tz=tz)
            return True
        except Exception:
            return None
    return False


def is_date(text: str, tz: str = "local") -> Tuple[bool, str]:
    """
    Check if text is a valid date. Format:
        format: "DD-MM-YYYY HH-mm-ss",
                "DD-MM-YYYY HH-mm",
                "DD-MM-YYYY HH",
                "DD-MM-YYYY"

    :param text: str: Text to
    :param tz: str:  (Default value = "local")

    """
    text = normalise_date(text)
    time_format_list = ["DD-MM-YYYY HH-mm-ss",
                        "DD-MM-YYYY HH-mm",
                        "DD-MM-YYYY HH",
                        "DD-MM-YYYY"]
    for fmt in time_format_list:
        try:
            from_format(text, fmt, tz=tz)
            return True, fmt
        except Exception:
            ...
    return False, ""
