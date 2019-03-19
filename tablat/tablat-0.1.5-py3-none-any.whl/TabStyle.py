# -*- coding: utf-8 -*-


class TabStyle(object):
    """
    Wrapper class to define the some style options for `Table` object.

    Attributes:
        borders (bool): `True` value to print borders around the table.
            Default value `True`
        row_sep (bool): `True` value to print a line to separate the rows.
            Default value `False`
        col_sep (bool): `True` value to print a vertical line to separate the
            data in a column. Default value `False`

    """

    def __init__(self, borders=True, row_sep=False, col_sep=False):
        self._borders = bool(borders)
        self._row_sep = bool(row_sep)
        self._col_sep = bool(col_sep)

    def update(self, borders=True, row_sep=False, col_sep=False):
        """
        Convinience method to update all wanted style options at once. If called
            without arguments, style object is reseted to default values.

        Args:
            borders (bool): `True` value to print borders around the table.
            row_sep (bool): `True` value to print a line to separate the rows.
            col_sep (bool): `True` value to print a vertical line to separate the
                data in a column
        """
        self._borders = bool(borders)
        self._row_sep = bool(row_sep)
        self._col_sep = bool(col_sep)

    @property
    def borders(self):
        """
        Define if borders around the table are printed
        """
        return self._borders

    @borders.setter
    def borders(self, borders):
        self._borders = bool(borders)

    @property
    def row_sep(self):
        """
        Define if a line is printed to separate the data of each column
        """
        return self._row_sep

    @row_sep.setter
    def row_sep(self, row_sep):
        self._row_sep = bool(row_sep)

    @property
    def col_sep(self):
        """
        Define if a line is printed to separate each row of the table
        """
        return self._col_sep

    @col_sep.setter
    def col_sep(self, col_sep):
        self._col_sep = bool(col_sep)
