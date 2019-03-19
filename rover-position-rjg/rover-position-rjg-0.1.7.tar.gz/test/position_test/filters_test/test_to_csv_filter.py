import os
import unittest
from typing import Iterable
from unittest.mock import patch, MagicMock

from rover_position_rjg.csv_helpers.csv_converter import TCsvItem, TObject
from rover_position_rjg.csv_helpers.csv_reader import CsvReader
from rover_position_rjg.position.filters.to_csv_filter import *


class TestConverter(CsvConverter[Data[float]]):

    def to_object(self, row: Iterable[TCsvItem]) -> TObject:
        values = list(row)
        return Data(float(values[0]), values[1])

    def to_row(self, value: Data[float]) -> Iterable[TCsvItem]:
        return [value.value, value.timestamp]


class ToCsvFilterTest(unittest.TestCase):
    filename = ...  # type: str

    def setUp(self):
        self.filename = 'csv_writer_test.csv'
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_saves_to_csv(self):
        values = [1.23, 4.56, 7.89]
        receiver = ToCsvFilter(TestConverter(), self.filename)
        try:
            for value in values:
                receiver.receive(Data(value, time.time()))
        except any:
            pass
        else:
            receiver.close()
        self.assertFileWritten(values)

    def test_ignores_receive_after_close(self):
        receiver = ToCsvFilter(TestConverter(), self.filename, 0.01)
        receiver.receive(Data(1.23, time.time()))
        receiver.close()
        receiver.receive(Data(4.56, time.time()))
        self.assertFileWritten([1.23])

    def test_ignores_receive_after_duration(self):
        receiver = ToCsvFilter(TestConverter(), self.filename, 0.01)
        try:
            receiver.receive(Data(1.23, time.time()))
            time.sleep(0.05)
            receiver.receive(Data(4.56, time.time()))
        except any:
            pass
        else:
            receiver.close()
        self.assertFileWritten([1.23])

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_scales_input(self, mock_filter: DataFilter[float,float]):
        mock_filter.receive = MagicMock()
        receiver = ToCsvFilter(TestConverter(), self.filename, 0.01)
        receiver.add(mock_filter)
        # Act
        data = Data(0.12345, 321)
        receiver.receive(data)
        # Assert
        mock_filter.receive.assert_called_once_with(data)

    def assertFileWritten(self, expected_values):
        with CsvReader(self.filename, TestConverter()) as reader:
            read_back_values = list(reader)
        floats = []
        for value in read_back_values:
            floats.append(value.value)
        self.assertEqual(expected_values, floats)


if __name__ == '__main__':
    unittest.main()
