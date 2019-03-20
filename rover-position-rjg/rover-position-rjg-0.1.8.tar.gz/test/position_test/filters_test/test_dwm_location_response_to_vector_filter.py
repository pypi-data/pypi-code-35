import unittest
from unittest.mock import MagicMock, patch

from decawave_1001_rjg import DwmPosition, DwmLocationResponse

from rover_position_rjg.data.data_filter import DataFilter, Data
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.filters.dwm_location_response_to_vector_filter import DwmLocationResponseToVectorFilter


class TestDwmLocationResponseToVectorFilter(unittest.TestCase):
    def test_constructor_sets_name(self):
        the_filter = DwmLocationResponseToVectorFilter('my name')
        self.assertEqual('my name', the_filter.name)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_sends_tag_location(self, mock_filter: DataFilter[Vector, Vector]):
        mock_filter.receive = MagicMock()
        the_filter = DwmLocationResponseToVectorFilter()
        the_filter.add(mock_filter)
        tag_position = [1500, 2200, 3300]
        dwm_tag_position = DwmPosition.from_properties(tag_position, 100)
        response = DwmLocationResponse.from_properties(dwm_tag_position, [])
        # Act
        data = Data(response, 456)
        the_filter.receive(data)
        # Assert
        expected_position = Vector([1.5, 2.2, 3.3])
        mock_filter.receive.assert_called_once_with(Data(expected_position, 456))
