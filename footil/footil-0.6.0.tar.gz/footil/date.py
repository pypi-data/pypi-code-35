"""Helpers for date manipulation."""
import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional

DATE_FMT = '%Y-%m-%d'
DATETIME_FMT = '%Y-%m-%d %H:%M:%S'


def _modify_date(
    dt: str,
    fmt: str,
    modify_fun: callable,
    new_fmt: Optional[str] = False,
    args: Optional[tuple] = None,
        kwargs: Optional[dict] = None) -> str:
    if not args:
        args = []
    if not kwargs:
        kwargs = {}
    if not new_fmt:
        new_fmt = fmt
    dt = datetime.datetime.strptime(dt, fmt)
    modified_dt = modify_fun(dt, *args, **kwargs)
    return modified_dt.strftime(new_fmt)


def get_first_day_date(
    dt: str,
    fmt: Optional[str] = DATE_FMT,
    new_fmt: Optional[str] = False,
        months: int = 0) -> str:
    """Return date by replacing day to be first day of the month.

    Args:
        dt (str): date string to modify
        fmt (str): format to convert from (default: {DATE_FMT})
        new_fmt (str): format to convert to. If not set, will use
            fmt variable format. (default: {False})
        months (int): x month
            (0 - this month, 1 - next month, -1 - last month, ...)

    Returns:
        str: modified date with day being first of the month.

    """
    return _modify_date(
        dt,
        fmt,
        lambda dt: dt + relativedelta(day=1, months=months),
        new_fmt=new_fmt)


def get_last_day_date(
    dt: str,
    fmt: Optional[str] = DATE_FMT,
    new_fmt: Optional[str] = False,
        months: int = 0) -> str:
    """Return date by replacing day to be last day of the month.

    Args:
        dt (str): date string to modify
        fmt (str): format to convert from (default: {DATE_FMT})
        new_fmt (str): format to convert to. If not set, will use
            fmt variable format. (default: {False})
        months (int): x month
            (0 - this month, 1 - next month, -1 - last month, ...)

    Returns:
        str: modified date with day being last of the month.

    """
    return _modify_date(
        dt,
        fmt,
        lambda dt: dt + relativedelta(day=1, days=-1, months=(months + 1)),
        new_fmt=new_fmt)
