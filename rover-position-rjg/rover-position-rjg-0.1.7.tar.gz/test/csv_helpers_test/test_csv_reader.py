import inspect
import os
import unittest
from typing import Iterable
from rover_position_rjg.csv_helpers.csv_converter import CsvConverter, TObject, TCsvItem
from rover_position_rjg.csv_helpers.csv_reader import CsvReader


class TestConverter(CsvConverter[float]):

    def to_object(self, row: Iterable[TCsvItem]) -> TObject:
        values = list(row)
        return float(values[0])

    def to_row(self, value: TObject) -> Iterable[TCsvItem]:
        return [value]


class CsvReaderTest(unittest.TestCase):
    filename = ...  # type: str

    def setUp(self):
        dir_name = os.path.dirname(inspect.getfile(CsvReaderTest))
        self.filename = os.path.join(dir_name, 'csv_reader_test.csv')

    def test_as_iterable(self):
        with CsvReader(self.filename, TestConverter()) as reader:
            items = list(reader)
        self.assertEqual(123.456, items[0])
        self.assertEqual(789.654, items[1])


if __name__ == '__main__':
    unittest.main()
