#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

class AdvertsTable:

    def __init__(self):
        self._data = []

    # TODO: redefine [x,y] operator (as in numpy)
    def get_data(self, row_index, column_index):
        return self._data[row_index][column_index]

    # TODO: redefine [x,y] operator (as in numpy)
    def set_data(self, row_index, column_index, value):
        if value is not None and not isinstance(value, self.dtype[column_index]):
            raise ValueError("Error at row {} column {} with value {}. Expect {} instance. Got {}".format(row_index, column_index, value, self.dtype[column_index], type(value)))

        self._data[row_index][column_index] = value

    def append(self, row):
        row_index = self.num_rows - 1
        self.insert_row(row_index, row=row)

    def insert_row(self, row_index, row=None):
        if row is None:
            row = list(self.default_values)

        self._data.insert(row_index, [None for i in range(self.num_columns)])

        for column_index in range(self.num_columns):
            self.set_data(row_index, column_index, row[column_index])

    def remove_row(self, index):
        if self.num_rows > 0:
            _removed = self._data.pop(index)

    @property
    def num_rows(self):
        return len(self._data)

    @property
    def num_columns(self):
        return len(self.headers)

    @property
    def shape(self):
        return (self.num_rows, self.num_columns)

    @property
    def headers(self):
        return ("Date",
                "Wake up",
                "Wake up duration",
                "Left home for school",
                "RER departure",
                "W. in",
                "W. out",
                "Back home",
                "Sleep",
                "Falling asleep duration")

    @property
    def default_values(self):
        return (datetime.datetime.now().date(),
                datetime.time(hour=6, minute=45),
                datetime.time(hour=0, minute=15),
                datetime.time(hour=8, minute=15),
                datetime.time(hour=8, minute=35),
                datetime.time(hour=9, minute=15),
                datetime.time(hour=18, minute=30),
                datetime.time(hour=19, minute=15),
                datetime.time(hour=22, minute=30),
                datetime.time(hour=0, minute=15))

    @property
    def dtype(self):
        return (datetime.date,
                datetime.time,
                datetime.time,
                datetime.time,
                datetime.time,
                datetime.time,
                datetime.time,
                datetime.time,
                datetime.time,
                datetime.time)
