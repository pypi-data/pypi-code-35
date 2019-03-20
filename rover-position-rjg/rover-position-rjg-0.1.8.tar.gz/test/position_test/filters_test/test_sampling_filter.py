import unittest
from unittest.mock import MagicMock, patch

from rover_position_rjg.position.filters.sampling_filter import *


class SamplingFilterTest(unittest.TestCase):
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_forwards_first_message(self, mock_filter: DataFilter[str,str]):
        mock_filter.receive = MagicMock()
        the_filter = SamplingFilter[str](5)
        the_filter.add(mock_filter)
        # Act
        the_filter.receive(Data('one', 123))
        the_filter.receive(Data('two', 123))
        # Assert
        mock_filter.receive.assert_called_once_with(Data('one', 123))

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_forwards_another_message_after_appropriate_period(self, mock_filter: DataFilter[str,str]):
        mock_filter.receive = MagicMock()
        the_filter = SamplingFilter[str](5)
        the_filter.add(mock_filter)
        # Act
        the_filter.receive(Data('one', 123))
        the_filter.receive(Data('two', 123))
        the_filter.receive(Data('three', 123))
        time.sleep(1/5 + 0.0001)
        the_filter.receive(Data('four', 123))
        the_filter.receive(Data('five', 123))
        # Assert
        self.assertEqual(2, mock_filter.receive.call_count)
        mock_filter.receive.assert_called_with(Data('four', 123))


if __name__ == '__main__':
    unittest.main()

