import math
import unittest
from typing import List
from unittest.mock import MagicMock, patch, call
from callee import Matcher
from decawave_1001_rjg import DwmLocationResponse, DwmPosition, DwmDistanceAndPosition

from rover_position_rjg.position.calibration.decawave.decawave_range_scaler import DecawaveRangeScaler
from rover_position_rjg.position.filters.decawave_to_position_in_filter import *
from rover_position_rjg.position.filters.decawave_trilateration_filter import DecawaveTrilaterationFilter


class LocationResponseMatcher(Matcher):
    def __init__(self, expected: Data[DwmLocationResponse]):
        self.expected = expected

    def match(self, data: Data[DwmLocationResponse]):
        actual = data.value
        expected = self.expected.value
        timestamps_match = self.expected.timestamp == data.timestamp
        tag_position_matches = self.position_matches(expected.get_tag_position(), actual.get_tag_position())
        anchors_match = expected.num_anchors == actual.num_anchors
        if anchors_match:
            expected_anchors = expected.get_anchor_distances_and_positions()
            actual_anchors = actual.get_anchor_distances_and_positions()
            for i in range(0, len(expected_anchors)):
                ea = expected_anchors[i]
                aa = actual_anchors[i]
                anchors_match = anchors_match and \
                                self.position_matches(ea.position(), aa.position()) and \
                                ea.quality_factor() == aa.quality_factor() and \
                                ea.address() == aa.address() and \
                                ea.distance() == aa.distance()
        return timestamps_match and tag_position_matches and anchors_match

    @staticmethod
    def position_matches(expected: DwmPosition, actual: DwmPosition):
        return expected.position() == actual.position() and \
               expected.quality_factor() == actual.quality_factor()


class TestDecawaveTrilaterationFilter(unittest.TestCase):
    def setUp(self):
        self.perfect = 100
        self.anchor_positions = {
            'DC00': DwmPosition.from_properties([0, 0, 500], 100),
            'DC01': DwmPosition.from_properties([4000, 0, 500], 100),
            'DC02': DwmPosition.from_properties([4000, 3000, 500], 100),
            'DC03': DwmPosition.from_properties([0, 3000, 500], 100),
        }

    @patch('rover_position_rjg.position.calibration.decawave.decawave_range_scaler.DecawaveRangeScaler')
    def test_constructor_sets_name(self, mock_scaler: DecawaveRangeScaler):
        the_filter = DecawaveTrilaterationFilter(mock_scaler, 'trilateration')
        self.assertEqual('trilateration', the_filter.name)

    @patch('rover_position_rjg.position.calibration.decawave.decawave_range_scaler.DecawaveRangeScaler')
    def test_scales_distances(self, mock_scaler: DecawaveRangeScaler):
        mock_scaler.scale = MagicMock(return_value=100)
        the_filter = DecawaveTrilaterationFilter(mock_scaler)
        # Act
        source = self.build_location_response(['DC00', 'DC01', 'DC02'], [1000, 2000, 3000])
        data = Data(source, 456)
        the_filter.receive(data)
        # Assert
        reference_temp = DecawaveRangeScaler.reference_temp
        mock_scaler.scale.assert_has_calls([
            call(1000, reference_temp, reference_temp, 'DC00'),
            call(2000, reference_temp, reference_temp, 'DC01'),
            call(3000, reference_temp, reference_temp, 'DC02')
        ])

    @patch('rover_position_rjg.position.calibration.decawave.decawave_range_scaler.DecawaveRangeScaler')
    def test_passes_temperatures_to_scaler(self, mock_scaler: DecawaveRangeScaler):
        mock_scaler.scale = MagicMock(return_value=100)
        the_filter = DecawaveTrilaterationFilter(mock_scaler)
        tag_temp = 20.5
        anchor_temp = 8.0
        # Act
        the_filter.set_temperatures(tag_temp, anchor_temp)
        source = self.build_location_response(['DC00', 'DC01', 'DC02'], [1000, 2000, 3000])
        data = Data(source, 456)
        the_filter.receive(data)
        # Assert
        mock_scaler.scale.assert_has_calls([
            call(1000, tag_temp, anchor_temp, 'DC00'),
            call(2000, tag_temp, anchor_temp, 'DC01'),
            call(3000, tag_temp, anchor_temp, 'DC02')
        ])

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    @patch('rover_position_rjg.position.calibration.decawave.decawave_range_scaler.DecawaveRangeScaler')
    def test_includes_scaled_distances_in_sent_message(self, mock_filter: DataFilter[DwmLocationResponse, DwmLocationResponse], mock_scaler: DecawaveRangeScaler):
        mock_filter.receive = MagicMock()
        mock_scaler.scale = MagicMock()
        mock_scaler.scale.side_effect = [1200, 2200, 3300]
        the_filter = DecawaveTrilaterationFilter(mock_scaler)
        the_filter.add(mock_filter)
        # Act
        source = self.build_location_response(['DC00', 'DC01', 'DC02'], [1000, 2000, 3000])
        data = Data(source, 456)
        the_filter.receive(data)
        # Assert
        expected = self.build_location_response(['DC00', 'DC01', 'DC02'], [1200, 2200, 3300], Vector([1697, 528, 500]))
        matcher = LocationResponseMatcher(Data(expected, 456))
        mock_filter.receive.assert_called_once_with(matcher)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    @patch('rover_position_rjg.position.calibration.decawave.decawave_range_scaler.DecawaveRangeScaler')
    def test_receive_calculates_position(self, mock_filter: DataFilter[DwmLocationResponse, DwmLocationResponse], mock_scaler: DecawaveRangeScaler):
        mock_filter.receive = MagicMock()
        mock_scaler.scale = MagicMock()
        d0 = round(1000 * math.sqrt(2))
        d1 = round(1000 * math.sqrt(10))
        d2 = round(1000 * math.sqrt(13))
        d3 = round(1000 * math.sqrt(5))
        mock_scaler.scale.side_effect = [d0, d1, d2, d3]
        the_filter = DecawaveTrilaterationFilter(mock_scaler)
        the_filter.add(mock_filter)
        # Act
        source = self.build_location_response(['DC00', 'DC01', 'DC02', 'DC03'], [d0, d1, d2, d3], Vector([500, 100, 10]))
        data = Data(source, 456)
        the_filter.receive(data)
        # Assert
        expected = self.build_location_response(['DC00', 'DC01', 'DC02', 'DC03'], [d0, d1, d2, d3], Vector([1000, 1000, 500]))
        matcher = LocationResponseMatcher(Data(expected, 456))
        mock_filter.receive.assert_called_once_with(matcher)

    def build_location_response(self, addresses: List[str],  measured_distances: List[int], position: Vector = Vector.zero()) -> DwmLocationResponse:
        tag_position = DwmPosition.from_properties(position.values, self.perfect)
        anchors = []
        for i in range(0, len(addresses)):
            address = addresses[i]
            dp = DwmDistanceAndPosition.from_properties(address, measured_distances[i], self.perfect, self.anchor_positions[address])
            anchors.append(dp)
        return DwmLocationResponse.from_properties(tag_position, anchors)
