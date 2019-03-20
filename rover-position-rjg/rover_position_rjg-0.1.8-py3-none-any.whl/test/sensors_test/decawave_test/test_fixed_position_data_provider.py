import unittest
from typing import List

from decawave_1001_rjg import DwmDistanceAndPosition

from rover_position_rjg.sensors.decawave.fixed_position_data_provider import FixedPositionDataProvider


class TestFixedPositionDataProvider(unittest.TestCase):
    def test_get_returns_suitable_tag_position(self):
        provider = FixedPositionDataProvider(100)
        result = provider.get()
        response = result.value
        self.assertEqual([0, 0, 0], response.get_tag_position().position())
        self.assertEqual(100, response.get_tag_position().quality_factor())

    def test_get_returns_known_anchors(self):
        provider = FixedPositionDataProvider(100)
        result = provider.get()
        response = result.value
        dps = response.get_anchor_distances_and_positions()
        self.assert_distance_and_position(dps[0], '1A85', 0, [0, 0, 0])
        self.assert_distance_and_position(dps[1], '559C', 4000, [4000, 0, 0])
        self.assert_distance_and_position(dps[2], 'DB08', 5000, [4000, 3000, 0])
        self.assert_distance_and_position(dps[3], '812E', 3000, [0, 3000, 0])

    def assert_distance_and_position(self, dp: DwmDistanceAndPosition, address: str, distance: int, position: List[int]):
        self.assertEqual(address, dp.address())
        self.assertEqual(distance, dp.distance())
        self.assertEqual(position, dp.position().position())
