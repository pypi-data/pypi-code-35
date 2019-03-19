import unittest
from unittest.mock import MagicMock, patch

from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.filters.position_filter import *
from rover_position_rjg.position.position.position_algorithm import *


class TestAlgorithm(PositionAlgorithm, ABC):
    def __init__(self, result: Position):
        super().__init__()
        self.result = result

    def step(self, data: PositionInput) -> Position:
        return self.result


class PositionFilterTest(unittest.TestCase):
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_step_calls_algorithm(self, mock_filter: DataFilter[Vector, Vector]):
        mock_filter.receive = MagicMock()
        position = Position(Quaternion.identity(), Vector.zero(), Vector.one(), Vector.zero())
        the_filter = PositionFilter(TestAlgorithm(position))
        the_filter.add(mock_filter)
        # Act
        data = PositionInput(velocity=Data(Vector.one(), 123))
        the_filter.receive(Data(data, 456))
        # Assert
        self.assertEqual(1, mock_filter.receive.call_count)
        mock_filter.receive.assert_called_once_with(Data(position, 456))


if __name__ == '__main__':
    unittest.main()

