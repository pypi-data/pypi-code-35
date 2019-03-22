# -*- python-indent-offset: 4; -*-

import calendar
from datetime import datetime
from os import listdir
from os.path import abspath, expanduser, getsize, isfile, join, splitext

import unijson
from dateutil.parser import parse
from dateutil.rrule import DAILY, MONTHLY, rrule

from .entry import Entry


class Entries(object):
    """A collection of Pomwarrior entries.

    This class implements the Active Record pattern:
    Entries contains a month of sorted list of Entry Objects. (Entry is sorted by its Date and UUID)

    Args:
        path (str): The path to the data files directory
        entries (list of :Entry:): A list of entries (use this when not loading data from files)
        load_from_file (bool): Should the data be loaded from the filesystem
        filter (date): Load data after the given date
    """

    def __init__(self, path="~/.config/pomw/data", entries=[], load=True):
        self.__path = path
        self.__entries = []
        if load:
            abs_path = abspath(expanduser(path))
            for file_name in sorted(listdir(abs_path)):
                # ignore non-json files
                if splitext(file_name)[1] == ".json":
                    loaded = Entries.load(join(abs_path, file_name))
                    self.entries += loaded
        else:
            self.entries = entries

    @property
    def entries(self):
        return self.__entries

    @entries.setter
    def entries(self, entries):
        self.__entries = []
        if not isinstance(entries, list):
            raise TypeError("'entries' should be a %s" % (list.__name__))

        for entry in entries:
            if isinstance(entry, dict):
                self.entries.append(
                    Entry(
                        uuid=entry.get("uuid"),
                        date=entry.get("date"),
                        planned=entry.get("planned", 0),
                        intervals=entry.get("intervals", []),
                    )
                )
            elif isinstance(entry, Entry):
                self.entries.append(entry)
            else:
                raise TypeError(
                    '"entries" elements should be of type %s' % (Entry.__name__)
                )
        self.entries.sort()

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, key):
        return self.entries[key]

    def find(self, uuid=None, date=None):
        """Find the matching Entry for the given uuid and date

        Arguments:
            uuid (str) or list of str: The uuid(s) to match
            date (datetime.date) or list of `datetime.date`: The date(s) to match

        Returns:
            A list of Entries matching both criteria (AND) is returned
        """
        uuid_criteria = None
        date_criteria = None
        if uuid:
            uuid_criteria = uuid if isinstance(uuid, list) else [uuid]

        if date:
            date_criteria = date if isinstance(date, list) else [date]

        return_list = []

        for entry in self.entries:
            if (not uuid_criteria or entry.uuid in uuid_criteria) and (
                not date_criteria or entry.date in date_criteria
            ):
                return_list += [entry]

        return return_list

    def insert(self, entry):
        self.entries.append(entry)

    @staticmethod
    def load(file_name):
        """Load Pomodoro data from a file

        Arguments: file_name (str): The file to load the data from

        Returns:
            List of Entry objects
        """
        try:
            fp = open(file_name, "r")

            # edge case when file has been created, but is empty
            if getsize(file_name) == 0:
                return []

            return unijson.load(fp)
        except FileNotFoundError:
            return []

    def save(self, path=None):
        """Save Pomodoro data to a file

        Arguments: path (str): The file to save the data to

        Returns:
            List of Entry objects
        """
        if not path:
            path = self.__path

        first_month = datetime(self.entries[0].date.year, self.entries[0].date.month, 1)
        last_month = datetime(
            self.entries[-1].date.year,
            self.entries[-1].date.month,
            calendar.monthrange(
                self.entries[-1].date.year, self.entries[-1].date.month
            )[1],
            23,
            59,
            59,
        )

        for dt in rrule(MONTHLY, dtstart=first_month, until=last_month):
            days = [
                dt2.date()
                for dt2 in list(
                    rrule(
                        DAILY,
                        dtstart=dt,
                        count=calendar.monthrange(dt.year, dt.month)[1],
                    )
                )
            ]

            entries = self.find(date=days)

            file_name = join(
                abspath(expanduser(path)), "%s.json" % (dt.strftime("%Y-%m"))
            )
            with open(file_name, "w") as file:
                unijson.dump(entries, file)

    def intervals(self):
        intervals = []
        for entry in self.entries:
            intervals += entry.intervals
        intervals.sort(reverse=True)
        return intervals

    def __repr__(self):
        return_text = "[\n"
        for entry in self.entries:
            return_text += "  " + str(entry) + "\n"
        return_text += "]"
        return return_text
