from datetime import datetime
from dateutil.utils import today
from pandas import date_range

from . import __version__


DATE_FORMAT_SOURCE = '%b %d, %Y'
DATE_FORMAT_TARGET = '%Y-%m-%d'
SOURCE_REV = __version__

def _transform_date(date_string):
    date_obj = datetime.strptime(date_string, DATE_FORMAT_SOURCE)

    return date_obj.strftime(DATE_FORMAT_TARGET)

def _isoformat_date(date):
    return date.isoformat()


def format_date(date, isoformat=False):
    if isoformat:
        return _isoformat_date(date=date)
    else:
        return date.strftime(DATE_FORMAT_TARGET)

def format_today(isoformat=False):
    return format_date(date=today(), isoformat=isoformat)

def get_date_range(default_start, default_end, start=None, end=None):
    _today = format_today()
    range_start = (start if start
                   else (default_start if default_start
                         else _today))
    range_end = (end if end
                 else (default_end if default_end
                       else _today))

    range_dates = date_range(start=range_start, end=range_end)

    return range_start, range_end, range_dates
