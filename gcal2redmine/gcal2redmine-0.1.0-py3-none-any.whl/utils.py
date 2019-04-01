#!/usr/bin/env python3

from datetime import datetime
from re import sub

import click


def format_date(date_time):
    """Convert gcal date into datetime object."""

    return datetime.strptime(sub(r"\+\d+:\d+$", "", date_time), "%Y-%m-%dT%H:%M:%S")


def validate_date(ctx, param, value):
    try:
        if value.lower() in ("today", "yesterday"):
            return value.lower()
        else:
            y, m, d = map(int, value.split("-"))
            return (y, m, d)
    except ValueError:
        raise click.BadParameter("must be YYYY-MM-DD, today, yesterday")


def strike(text):
    result = str()
    for c in text:
        result += c + "\u0336"
    return result
