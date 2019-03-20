import unittest
from unittest.mock import MagicMock, patch

from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.filters.scaling_filter import *


class TestScaler(Scaler[Vector]):
    def __init__(self):
        self._offset = Vector([1, 3, 6])

    def scale(self, data: Data[Vector]) -> Data[Vector]:
        scaled = data.value - self._offset
        return Data(scaled, data.timestamp)


class ScalingFilterTest(unittest.TestCase):
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_scales_input(self, mock_filter: DataFilter[Vector,Vector]):
        mock_filter.receive = MagicMock()
        the_filter = ScalingFilter(TestScaler())
        the_filter.add(mock_filter)
        # Act
        data = Data(Vector([10, 11, 12]), 123)
        the_filter.receive(data)
        # Assert
        mock_filter.receive.assert_called_once_with(Data(Vector([9, 8, 6]), 123))


if __name__ == '__main__':
    unittest.main()
