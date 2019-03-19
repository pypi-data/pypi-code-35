import unittest

from rover_position_rjg.position.calibration.decawave.two_way_ranging_calibration import TwoWayRangingCalibration


class TestTwoWayRangingCalibration(unittest.TestCase):
    def test_can_get_properties(self):
        twr = TwoWayRangingCalibration('DECA', 1.23, 4.56)
        self.assertEqual('DECA', twr.address)
        self.assertEqual(1.23, twr.signal_level_bias)
        self.assertEqual(4.56, twr.range_bias)