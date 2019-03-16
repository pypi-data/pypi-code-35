"""
Utility classes for the application
"""
import re
from datetime import datetime
from datetime import timedelta
from lambdabase.Constants import Constants


class Utils(object):
    """
    The main utility class
    """
    FORMAT_DURATION = 'PT(?:(\d+)H)*(?:(\d+)M)*(?:(\d+)S)*'

    @classmethod
    def dt2str(cls, data, date_format=Constants.DATETIME_FORMAT_INTERNAL):
        """
        Safely converts a string to a datetime. Return None if not possible
        """
        if not data:
            return None

        try:
            value = data.strftime(date_format)
        except (ValueError, AttributeError):
            value = None

        return value

    @classmethod
    def str2dt(cls, data, date_format=Constants.DATETIME_FORMAT_INTERNAL):
        """
        Safely converts a string to a datetime. Return None if not possible
        """
        if not data:
            return None

        try:
            value = datetime.strptime(data, date_format)
        except ValueError:
            value = None

        return value

    @classmethod
    def td2json(cls, data):
        """
        Converts a timedelta in a json serialisable format
        """
        if not isinstance(data, timedelta):
            return None
        return data.total_seconds()

    @classmethod
    def json2td(cls, data):
        """
        Converts a timedelta in a json serialisable format
        """
        td = timedelta(seconds=data)
        return td

    @classmethod
    def td2str(cls, data):
        """
        Converts a timedelta into friendly formatted string
        """
        if not isinstance(data, timedelta):
            return None

        hours, minutes, seconds = Utils.splittd(data)

        if hours == 0:
            return "{0}:{1}".format(minutes, seconds)
        else:
            return "{0}:{1}:{2}".format(hours, minutes, seconds)

    @classmethod
    def str2td(cls, data):
        """
        Converts a duration in iso8601 format as returned
        by youtube into a timedelta
        """
        hrs, mins, secs = re.match(Utils.FORMAT_DURATION, data).groups()
        hrs = hrs if hrs else 0
        mins = mins if mins else 0
        secs = secs if secs else 0
        return timedelta(hours=int(hrs), minutes=int(mins), seconds=int(secs))

    @classmethod
    def splittd(cls, data):
        """
        Splits a timedelta into component parts
        """
        if not isinstance(data, timedelta):
            return None

        hours, remainder = divmod(data.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return hours, minutes, seconds
