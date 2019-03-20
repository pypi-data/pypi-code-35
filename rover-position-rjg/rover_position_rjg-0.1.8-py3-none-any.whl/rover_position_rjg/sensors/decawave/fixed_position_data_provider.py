import time

from decawave_1001_rjg import DwmLocationResponse, DwmPosition, DwmDistanceAndPosition

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.data_pump.rate_limited_data_provider import RateLimitedDataProvider


class FixedPositionDataProvider(RateLimitedDataProvider[DwmLocationResponse]):
    def __init__(self, frequency: float):
        super().__init__(frequency)
        self.qf = 100
        self.pos0 = DwmPosition.from_properties([0, 0, 0], self.qf)
        self.pos1 = DwmPosition.from_properties([4000, 0, 0], self.qf)
        self.pos2 = DwmPosition.from_properties([4000, 3000, 0], self.qf)
        self.pos3 = DwmPosition.from_properties([0, 3000, 0], self.qf)

    def get(self) -> Data[DwmLocationResponse]:
        timestamp = self.time()
        anchors = [
            DwmDistanceAndPosition.from_properties('1A85', 0, self.qf, self.pos0),
            DwmDistanceAndPosition.from_properties('559C', 4000, self.qf, self.pos1),
            DwmDistanceAndPosition.from_properties('DB08', 5000, self.qf, self.pos2),
            DwmDistanceAndPosition.from_properties('812E', 3000, self.qf, self.pos3),
        ]
        tag_position = DwmPosition.from_properties([0, 0, 0], self.qf)
        response = DwmLocationResponse.from_properties(tag_position, anchors)
        return Data(response, timestamp)

    def close(self):
        pass

    @staticmethod
    def time():
        return time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW) * 1e-9