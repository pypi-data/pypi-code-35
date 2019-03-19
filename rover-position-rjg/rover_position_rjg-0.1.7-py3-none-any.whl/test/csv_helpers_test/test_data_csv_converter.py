import unittest

from rover_position_rjg.csv_helpers.data_csv_converter import *


class StringConverter(CsvConverter[str]):

    def to_row(self, value: str) -> Iterable[TCsvItem]:
        return [value]

    def to_object(self, row: Iterable[TCsvItem]) -> str:
        for value in row:
            return value


class TestDataCsvConverter(unittest.TestCase):
    def test_convert_object_to_row(self):
        converter = DataCsvConverter(StringConverter())
        row = converter.to_row(Data('Blue', 123))
        self.assertEqual(['Blue', 123], row)

    def test_convert_row_to_object(self):
        converter = DataCsvConverter(StringConverter())
        the_object = converter.to_object(['Blue', 123])
        self.assertEqual(Data('Blue', 123), the_object)

    def test_convert_row_to_object_2(self):
        converter = DataCsvConverter(StringConverter())
        the_object = converter.to_object(['Blue', '123'])
        self.assertEqual(Data('Blue', 123), the_object)
