from openpyxl import load_workbook
import logging
import itertools

from .utils import (
    enumerate_phone_column_index_from_row, get_cell_values_from_row
)

log = logging.getLogger(__name__)


class Sheet:
    phone_column_index = -1

    valid_rows = []
    invalid_rows = []

    def _enumerate_phone_column(self):
        # get first two rows from sheet
        rows = self.sheet[1:2]

        # this will loop through the first two rows and set the
        # phone_column_index only when it's first enumerated
        for row in rows:
            value = enumerate_phone_column_index_from_row(row)

            if value is not -1 and self.phone_column_index is -1:
                self.phone_column_index = value
                break

        # raise an exception if the value wasn't enumerated
        if self.phone_column_index is -1:
            raise Exception("phone_column_index couldn't be enumerated")

        log.debug('phone_column_index enumerated at {}'
                  .format(self.phone_column_index))

    def __init__(self, sheet):
        self.sheet = sheet

        self._enumerate_phone_column()

        log.debug(self.__dict__)

    def get_row_values(self):
        return [get_cell_values_from_row(row) for row in self.sheet.rows]


class Workbook:
    def __init__(self, workbook_file_path):
        self.workbook = load_workbook(workbook_file_path,
                                      read_only=True)

        self.sheets = [Sheet(sheet) for sheet in self.workbook]

        log.debug(self.__dict__)

    def get_sheet_rows(self):
        values = [sheet.get_row_values() for sheet in self.sheets]

        return list(itertools.chain.from_iterable(values))
