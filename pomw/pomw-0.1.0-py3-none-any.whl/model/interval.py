# -*- python-indent-offset: 4; -*-

from abc import ABC
from datetime import datetime


class Interval(ABC):
    def __init__(self, start_time=None, end_time=None):
        self.start_time = start_time
        self.end_time = end_time

    @staticmethod
    def __json_decode__(d):
        return Interval(
            start_time=d.get("_Interval__start_time", None),
            end_time=d.get("_Interval__end_time", None),
        )

    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, start_time):
        if isinstance(start_time, datetime):
            self.__start_time = start_time
        elif not start_time:
            self.__start_time = None
        else:
            raise TypeError("'start_time' should be of type %s" % (datetime.__name__))

    @property
    def end_time(self):
        return self.__end_time

    @end_time.setter
    def end_time(self, end_time):
        if isinstance(end_time, datetime):
            self.__end_time = end_time
        elif not end_time:
            self.__end_time = None
        else:
            raise TypeError("'end_time' should be of type %s" % (datetime.__name__))

    def __lt__(self, other):
        self_start = datetime.min
        self_end = datetime.min
        other_start = datetime.min
        other_end = datetime.min
        if self.start_time:
            self_start = self.start_time
        if self.end_time:
            self_end = self.end_time
        if other.start_time:
            other_start = other.start_time
        if other.end_time:
            other_end = other.end_time

        if self_start == other_start:
            return self_end < other_end
        return self_start < other_start

    def __repr__(self):
        return "{start_time: %s, end_time: %s}" % (self.start_time, self.end_time)
