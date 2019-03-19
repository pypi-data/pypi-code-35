import os
import unittest
from rover_position_rjg.csv_helpers.csv_converter import *
from rover_position_rjg.csv_helpers.csv_reader import CsvReader
from rover_position_rjg.csv_helpers.csv_writer import CsvWriter


class TestConverter(CsvConverter[float]):

    def to_object(self, row: Iterable[TCsvItem]) -> TObject:
        values = list(row)
        return float(values[0])

    def to_row(self, value: TObject) -> Iterable[TCsvItem]:
        return [value]


class CsvWriterTest(unittest.TestCase):
    filename = ...  # type: str

    def setUp(self):
        self.filename = 'csv_writer_test.csv'
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_as_iterable(self):
        values = [1.23, 4.56, 7.89]
        with CsvWriter(self.filename, TestConverter()) as writer:
            for value in values:
                writer.write(value)
        with CsvReader(self.filename, TestConverter()) as reader:
            read_back_values = list(reader)
            print(read_back_values)
        self.assertEqual(values, read_back_values)

    def test_with_open_close(self):
        values = [1.23, 4.56, 7.89]
        writer = CsvWriter(self.filename, TestConverter())
        writer.open()
        for value in values:
            writer.write(value)
        writer.close()
        with CsvReader(self.filename, TestConverter()) as reader:
            read_back_values = list(reader)
            print(read_back_values)
        self.assertEqual(values, read_back_values)


if __name__ == '__main__':
    unittest.main()
