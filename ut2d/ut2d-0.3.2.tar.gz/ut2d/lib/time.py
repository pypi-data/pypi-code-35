import time
from datetime import datetime, timedelta
from typing import Union

from .message import throw_msg
from .timezone_scrapper import to_utc_fmt, TimezoneScrapper


class Time:
    """A wrapper class providng all the functionalities supported by ut2d package.

    Args:
        ut: unix timestamp
    """

    def __init__(self, ut: Union[int, float]):
        self.ut_now = time.time()
        self.ut_local = self._convert_ut(ut)

        self.dt_now = datetime.now()
        self.dt_local = datetime.fromtimestamp(self.ut_local)
        self.dt_utc = datetime.utcfromtimestamp(self.ut_local)
    
    def _convert_ut(self, ut: Union[int, float]) -> float:
        """Convert input unix timstamp to 10-digit (in seconds)"""
        ut = float(ut)

        if ut <= 1e10:
            return ut
        elif ut > 1e12 and ut <= 1e13:
            return ut / 1000

    @staticmethod
    def is_valid(ut: Union[int, float]) -> bool:
        """Check if the input unix timestamp is either 10-digit (in seconds) or
        13-digit (in milliseconds).

        All other inputs are invalid.
        """
        try:
            ut = float(ut)
        except:
            return False

        if ut <= 1e10:
            return True
        elif ut > 1e12 and ut <= 1e13:
            return True
        else:
            return False

    @staticmethod
    def fmt(dt: datetime) -> str:
        """Format datetime to: day of week, date, time
        
        e.g. Sat, Mar 16, 2019 07:31PM
        """
        return dt.strftime('%a, %b %d, %Y %I:%M%p')

    @property
    def local(self) -> datetime:
        return self.dt_local

    @property
    def utc(self) -> datetime:
        return self.dt_utc

    @property
    def from_now(self) -> str:
        """Get the time difference (timedelta) from now"""
        if self.ut_now >= self.ut_local:
            diff = self.dt_now - self.dt_local
            ahead = False
        else:
            diff = self.dt_local - self.dt_now
            ahead = True
        
        d = diff.days
        h, _ = divmod(diff.seconds, 3600)
        m, s = divmod(_, 60)

        diff_fmt = f'Given time is {d} days, {h} hrs, {m} mins, {s} secs '
        diff_fmt += 'ahead' if ahead else 'ago'

        return diff_fmt

    def in_timezone(self, timezone: str) -> datetime:
        """Get the datetime in a given timezone"""
        timezone = to_utc_fmt(timezone)
        if timezone is None:
            throw_msg(1, 'tz_fmt_invalid', True)

        tz_sign = timezone[3]
        tz_diff = int(timezone[4:])

        if tz_sign == '-':
            dt = self.dt_utc.timestamp() - tz_diff * 3600
        elif tz_sign == '+':
            dt = self.dt_utc.timestamp() + tz_diff * 3600
        
        return datetime.fromtimestamp(dt)
    
    def in_city(self, city: str) -> datetime:
        """Get the datetime in a given city by first scrap the timezone
        info with a scrapper, then call the in_timezone method.
        """
        ts = TimezoneScrapper(city)

        if ts.timezone:
            return self.in_timezone(ts.timezone)
        else:
            throw_msg(0, 'search_tz_failed', 1)
