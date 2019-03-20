import time
from abc import ABC

from rover_position_rjg.data.data import Data, TValue
from rover_position_rjg.data.data_filter import DataFilter


class SamplingFilter(DataFilter[TValue, TValue], ABC):
    """A filter that only passes on a small subset of messages.
    Specify the required sampling frequency in the constructor. """

    def __init__(self, sampling_frequency: float):
        super().__init__()
        self._sampling_interval = 1 / sampling_frequency
        self._time_of_last_output = 0

    def receive(self, data: Data[TValue]) -> None:
        now = time.time()
        if now - self._time_of_last_output > self._sampling_interval:
            self._time_of_last_output = now
            self.send(data)
