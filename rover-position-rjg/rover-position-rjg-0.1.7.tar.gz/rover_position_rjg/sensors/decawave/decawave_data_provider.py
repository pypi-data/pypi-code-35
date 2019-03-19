import time

from decawave_1001_rjg import DwmLocationResponse, Decawave1001Driver

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.data_pump.data_provider import DataProvider


class DecawaveDataProvider(DataProvider[DwmLocationResponse]):
    def __init__(self):
        self.driver = Decawave1001Driver(22, 2)

    def get(self) -> Data[DwmLocationResponse]:
        timestamp = self.time()
        response = self.driver.get_loc()
        return Data(response, timestamp)

    def poll(self, timeout: float) -> bool:
        return self.driver.data_ready(int(timeout * 1000))

    def close(self):
        self.driver.close()

    @staticmethod
    def time():
        return time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW) * 1e-9