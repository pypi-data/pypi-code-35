#!/usr/bin/env python3

"""
Small module designed to convert duration to an understandable
human representation.
"""

from time import gmtime, strftime


def duration_to_date_and_time(duration_in_seconds: int) -> str:
    """
    Convert duration to a string: n days, HH:MM:SS.

    :param duration_in_seconds: Duration in seconds.
        max: 67767976233532799.
    """
    __check_if_negative(duration_in_seconds)
    dur_in_days = duration_to_int_days(duration_in_seconds)
    dur_to_time = duration_to_time(duration_in_seconds)
    if dur_in_days > 1:
        return f"{dur_in_days} days, {dur_to_time}"
    elif dur_in_days > 0:
        return f"{dur_in_days} day, {dur_to_time}"
    else:
        return f"{duration_to_time(duration_in_seconds)}"


def duration_to_int_days(duration_in_seconds: int) -> int:
    """
    Convert duration to int number of days.

    :param duration_in_seconds: Duration in seconds.
        max: 67767976233532799.
    """
    __check_if_negative(duration_in_seconds)
    return duration_in_seconds // 86400


def duration_to_time(duration_in_seconds: int) -> str:
    """
    Convert duration to HH:MM:SS.

    :param duration_in_seconds: Duration in seconds.
        max: 67767976233532799.
    """
    __check_if_negative(duration_in_seconds)
    return strftime("%H:%M:%S", gmtime(duration_in_seconds))


def __check_if_negative(duration_in_seconds: int) -> None:
    """
    Check if duration_in_seconds is negative.

    :param duration_in_seconds: Duration in seconds.
        max: 67767976233532799.
    """
    if duration_in_seconds < 0:
        raise ValueError("duration_in_seconds needs to be positive.")
