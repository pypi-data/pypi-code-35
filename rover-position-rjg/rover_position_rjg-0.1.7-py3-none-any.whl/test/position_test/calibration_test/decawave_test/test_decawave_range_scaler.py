import unittest

from rover_position_rjg.position.calibration.decawave.decawave_range_scaler import DecawaveRangeScaler
from rover_position_rjg.position.calibration.decawave.two_way_ranging_calibration import TwoWayRangingCalibration


class TestDecawaveRangeScaler(unittest.TestCase):
    neutral_range = 6317
    neutral_temp = 25

    def setUp(self):
        self.calibration_01 = TwoWayRangingCalibration('DECA_01', 0, 0)

    def test_scale_result_is_an_int(self):
        scaler = DecawaveRangeScaler(4.3, [self.calibration_01])
        temp = self.neutral_temp - 10
        result = scaler.scale(self.neutral_range, temp, temp, 'DECA_01')
        self.assertIsInstance(result, int)

    def test_temperature_sensitivity(self):
        scaler = DecawaveRangeScaler(4.3, [self.calibration_01])
        temp = self.neutral_temp - 10
        result = scaler.scale(self.neutral_range, temp, temp, 'DECA_01')
        self.assertEqual(43 + self.neutral_range, round(result))

    def test_temperature_bias_depends_on_average_temp(self):
        scaler = DecawaveRangeScaler(2, [self.calibration_01])
        tag_temp = self.neutral_temp - 10
        anchor_temp = self.neutral_temp - 20
        result = scaler.scale(self.neutral_range, tag_temp, anchor_temp, 'DECA_01')
        self.assertEqual(30 + self.neutral_range, round(result))

    def test_calculated_range_depends_on_received_signal_level_adjustment(self):
        scaler = DecawaveRangeScaler(2, [self.calibration_01])
        result = scaler.scale(4000, self.neutral_temp, self.neutral_temp, 'DECA_01')
        self.assertEqual(4000+51, round(result))

    def test_range_is_calibrated_by_anchor_received_signal_level_bias(self):
        calibration = TwoWayRangingCalibration('BEAT', -2.2, 0)
        scaler = DecawaveRangeScaler(2, [calibration])
        result = scaler.scale(4000, self.neutral_temp, self.neutral_temp, 'BEAT')
        self.assertEqual(4000+70, round(result))

    def test_anchor_range_bias_is_subtracted_from_range(self):
        calibration = TwoWayRangingCalibration('BEAT', 0, 789)
        scaler = DecawaveRangeScaler(2, [calibration])
        result = scaler.scale(self.neutral_range, self.neutral_temp, self.neutral_temp, 'BEAT')
        self.assertEqual(self.neutral_range-789, round(result))

    def test_picks_calibration_by_address(self):
        calibration2 = TwoWayRangingCalibration('BEAT', 0, 789)
        scaler = DecawaveRangeScaler(2, [calibration2, self.calibration_01])
        result = scaler.scale(self.neutral_range, self.neutral_temp, self.neutral_temp, 'DECA_01')
        self.assertEqual(self.neutral_range, round(result))

    def test_raises_exception_for_unknown_address(self):
        scaler = DecawaveRangeScaler(2, [self.calibration_01])
        with self.assertRaises(LookupError):
            scaler.scale(self.neutral_range, 0, 0, 'UNKNOWN')

    def test_can_scale_0_range(self):
        scaler = DecawaveRangeScaler(4.3, [self.calibration_01])
        result = scaler.scale(0, self.neutral_temp, self.neutral_temp, 'DECA_01')
        self.assertEqual(110, result)
