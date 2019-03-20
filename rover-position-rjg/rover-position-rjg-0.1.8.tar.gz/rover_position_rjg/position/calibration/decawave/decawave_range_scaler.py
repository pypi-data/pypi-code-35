import math
# from scipy import interpolate
from typing import List

import numpy as np

from rover_position_rjg.position.calibration.decawave.two_way_ranging_calibration import TwoWayRangingCalibration


class DecawaveRangeScaler:
    """Corrects the ranges reported by a pair of tags.
    Based on the following decaWave document
    APS011 Application Note
    Sources of Error in DW1000 Based Two-Way Ranging (TWR) Schemes
    Version 1.0
    https://www.decawave.com/sites/default/files/resources/aps011_sources_of_error_in_twr.pdf
    """
    rsl_biases = np.flip([-160, -130, -125, -120, -115, -110, -105, -100, -93, -82, -69, -51, -27,   0,  21,  35,  42,  49,  62,  71,  76,  81])
    rsl_levels = np.flip([ -39,  -53,  -55,  -57,  -59,  -61,  -63,  -65, -67, -69, -71, -73, -75, -77, -79, -81, -83, -85, -87, -89, -91, -93])
    reference_temp = 25 # Reference temperature in degrees centigrade
    p = -14.3           # Pt - transmitted power = -14.3 for DWM 1000
    g = 2.0             # G - sum of transmit and receive antenna gains - assume 1 dB each
    c = 299_792_458     # speed of light in m/s
    f = 6489_600_000    # centre frequency of the channel in Hz

    def __init__(self, temp_sensitivity: float, anchor_calibrations: List[TwoWayRangingCalibration]):
        """
        Creates a scaler from its calibration
        :param temp_sensitivity: range offset if millimetres per degree centigrade
        :param anchor_calibrations: calibrations for each tag/anchor pair
        """
        self.temp_sensitivity = temp_sensitivity
        self.anchor_calibrations = dict()
        for a in anchor_calibrations:
            self.anchor_calibrations[a.address] = a

    def scale(self, measured_range: int, tag_temp: float, anchor_temp: float, address) -> int:
        calibration = self.anchor_calibrations[address]
        rsl = self.calculate_received_signal_level(measured_range / 1000) - calibration.signal_level_bias
        bias = self.bias_from_received_signal_level(rsl)
        temp_bias = self.calculate_temperature_bias(tag_temp, anchor_temp)
        result = measured_range - bias - temp_bias - calibration.range_bias
        return int(round(result))

    def calculate_temperature_bias(self, tag_temp: float, anchor_temp: float):
        average_temp = (tag_temp + anchor_temp) / 2
        return (average_temp - self.reference_temp) * self.temp_sensitivity

    def calculate_received_signal_level(self, reported_range: float) -> float:
        reported_range = max([1, reported_range])
        return self.p + self.g + 20 * math.log(self.c, 10) - 20 * math.log((4 * math.pi * self.f * reported_range), 10)

    def bias_from_received_signal_level(self, rsl: float) -> float:
        return np.interp(rsl, self.rsl_levels, self.rsl_biases)
