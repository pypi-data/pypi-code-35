import unittest
from unittest.mock import MagicMock, patch

from callee import Matcher

from rover_position_rjg.data.flags import Flags
from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.position.filters.attitude_out_to_position_in_filter import *
from rover_position_rjg.position.position.position_algorithm import *


class PositionInputMatcher(Matcher):
    def __init__(self, value: Data[PositionInput]):
        self.expected = value

    def match(self, data: Data[PositionInput]):
        return self.expected.timestamp == data.timestamp and \
               data.value.position is None and \
               data.value.velocity is None and \
               self.expected.value.attitude.value.attitude == data.value.attitude.value.attitude and \
               self.expected.value.attitude.value.acceleration == data.value.attitude.value.acceleration and \
               self.expected.value.attitude.value.status == data.value.attitude.value.status


class AttitudeOutputToPositionInputFilterTest(unittest.TestCase):
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_receive_converts_data(self, mock_filter: DataFilter[Vector, Vector]):
        mock_filter.receive = MagicMock()
        g = 10
        the_filter = AttitudeOutputToPositionInputFilter(g)
        the_filter.add(mock_filter)
        # Act
        data = AttitudeOutput(Vector.one(), Quaternion.identity(), Flags(0x1A))
        the_filter.receive(Data(data, 456))
        # Assert
        expected = PositionInput(attitude=Data(AttitudeOutput(Vector([g, g, g]), Quaternion.identity(), Flags(0x1A)), 123))
        mock_filter.receive.assert_called_once_with(PositionInputMatcher(Data(expected, 456)))
