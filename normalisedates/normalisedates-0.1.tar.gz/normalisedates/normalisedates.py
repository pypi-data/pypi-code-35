#!/usr/bin/env python3

from pendulum import from_format


def normalise_date(text: str) -> str:
    """
    This function normalize text, is useful to normalize dates.

    :param text: str: String of date to normalise.
    """
    return text.replace(
        "/", "-").replace(
        ":", "-").replace(
        ".", "-").replace(
        "@", "-")
