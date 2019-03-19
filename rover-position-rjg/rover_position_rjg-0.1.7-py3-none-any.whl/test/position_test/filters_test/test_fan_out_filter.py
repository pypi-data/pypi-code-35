import unittest
from unittest.mock import patch, MagicMock

from rover_position_rjg.position.filters.fan_out_filter import *


class FanOutFilterTest(unittest.TestCase):
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_passes_data_to_filters(self, receiver_one: DataFilter[str,str], receiver_two: DataFilter[str,str]):
        receiver_one.receive = MagicMock()
        receiver_two.receive = MagicMock()
        the_filter = FanOutFilter()
        the_filter.add(receiver_one)
        the_filter.add(receiver_two)
        # Act
        data = Data('test', 123)
        the_filter.receive(data)
        # Assert
        receiver_one.receive.assert_called_once_with(data)
        receiver_two.receive.assert_called_once_with(data)
