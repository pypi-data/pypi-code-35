import unittest
from unittest.mock import MagicMock, patch
from callee import Matcher
from rover_position_rjg.position.filters.decawave_to_position_in_filter import *
from rover_position_rjg.position.position.position_algorithm import *


class PositionInputMatcher(Matcher):
    def __init__(self, value: Data[PositionInput]):
        self.expected = value

    def match(self, data: Data[PositionInput]):
        return self.expected.timestamp == data.timestamp and \
               data.value.attitude is None and \
               data.value.velocity is None and \
               self.expected.value.position.value == data.value.position.value and \
               self.expected.value.position.timestamp == data.value.position.timestamp


class DecawaveToPositionInputFilterTest(unittest.TestCase):
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_receive_converts_data(self, mock_filter: DataFilter[Vector, Vector]):
        mock_filter.receive = MagicMock()
        the_filter = DecawaveToPositionInputFilter()
        the_filter.add(mock_filter)
        # Act
        data = Data(Vector.one(), 456)
        the_filter.receive(data)
        # Assert
        expected = Data(PositionInput(None, None, data), data.timestamp)
        matcher = PositionInputMatcher(expected)
        mock_filter.receive.assert_called_once_with(matcher)


if __name__ == '__main__':
    unittest.main()

