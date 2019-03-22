# -*- python-indent-offset: 4; -*-

import datetime

import unijson

from .interval import Interval
from .pomodoro import Pomodoro


class Entry:
    """A Pomwarrior entry"""

    def __init__(
        self, uuid=None, date=datetime.datetime.now().date(), planned=0, intervals=[]
    ):
        self.uuid = uuid
        self.date = date
        self.planned = planned
        self.intervals = intervals

    @staticmethod
    def __json_decode__(d):
        intervals = []
        for c in d.get("_Entry__intervals", []):
            intervals.append(c)

        entry = Entry(
            uuid=d.get("_Entry__uuid", None),
            date=d.get("_Entry__date", None),
            planned=d.get("_Entry__planned", 0),
            intervals=intervals,
        )

        return entry

    @property
    def uuid(self):
        return self.__uuid

    @uuid.setter
    def uuid(self, uuid):
        self.__uuid = uuid

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        if not isinstance(date, datetime.date):
            raise TypeError("'date' should be of type %s" % (datetime.date.__name__))
        self.__date = date

    @property
    def planned(self):
        return self.__planned

    @planned.setter
    def planned(self, planned):
        self.__planned = planned

    @property
    def intervals(self):
        return self.__intervals

    @property
    def pomodoros(self):
        return list(
            filter(lambda interval: isinstance(interval, Pomodoro), self.__intervals)
        )

    @property
    def nonpomodoros(self):
        return list(
            filter(
                lambda interval: isinstance(interval, Interval)
                and not isinstance(interval, Pomodoro),
                self.__intervals,
            )
        )

    @intervals.setter
    def intervals(self, intervals):
        self.__intervals = []
        for interval in intervals:
            if isinstance(interval, dict):
                self.__entries.append(
                    Interval(
                        task=self.uuid,
                        start=interval.get("start", None),
                        end=interval.get("end", None),
                    )
                )
            elif isinstance(interval, Interval):
                interval.task = self.uuid
                self.__intervals.append(interval)
            else:
                raise TypeError('Unable to parse "interval"')

    def __repr__(self):
        return "{date: %s, uuid: %s, planned: %s, intervals: %s }" % (
            self.date,
            self.uuid,
            self.planned,
            self.intervals,
        )

    def __eq__(self, other):
        return self.date == other.date and self.uuid == other.uuid

    def __lt__(self, other):
        if self.date == other.date:
            return self.uuid < other.uuid
        return self.date < other.date
