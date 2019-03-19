import time
import unittest
from unittest.mock import MagicMock, patch
from rover_position_rjg.data.data import *
from rover_position_rjg.csv_helpers.csv_converter import CsvConverter
from rover_position_rjg.data.data_value_csv_converter import DataValueCsvConverter


class DataValueCsvConverterTest(unittest.TestCase):

    @patch('rover_position_rjg.csv_helpers.csv_converter.CsvConverter')
    def test_to_row_passes_value_to_underlying_converter(self, mock_converter: CsvConverter):
        mock_converter.to_row = MagicMock()
        data_value_csv_converter = DataValueCsvConverter(mock_converter)

        data = Data[str]("The Value", 1)
        data_value_csv_converter.to_row(data)

        mock_converter.to_row.assert_called_once_with("The Value")

    @patch('rover_position_rjg.csv_helpers.csv_converter.CsvConverter')
    def test_to_object_gets_value_from_underlying_converter(self, mock_converter: CsvConverter):
        mock_converter.to_object = MagicMock()
        mock_converter.to_object.return_value = 'Hello'
        data_value_csv_converter = DataValueCsvConverter(mock_converter)
        before = time.time()

        the_object = data_value_csv_converter.to_object(['Hello'])
        after = time.time()

        self.assertEqual('Hello', the_object.value)
        self.assertTrue(the_object.timestamp >= before)
        self.assertTrue(the_object.timestamp <= after)
        mock_converter.to_object.assert_called_once_with(['Hello'])


if __name__ == '__main__':
    unittest.main()
