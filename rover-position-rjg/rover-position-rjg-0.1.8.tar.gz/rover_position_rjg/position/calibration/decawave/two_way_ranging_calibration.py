class TwoWayRangingCalibration:
    def __init__(self, address: str, signal_level_bias: float, range_bias: float):
        self.address = address
        self.signal_level_bias = signal_level_bias
        self.range_bias = range_bias
