import time

from rover_position_rjg.data.data import TValue
from rover_position_rjg.data.data_pump.data_provider import *


class RateLimitedDataProvider(DataProvider[TValue], ABC):
    def __init__(self, frequency: float):
        """
        Specifies the output data rate in Hz
        :param frequency: the output data rate in Hz
        """
        self.interval = 1 / frequency
        self.start_time = time.time()
        self.count = 0

    def poll(self, timeout: float) -> bool:
        current_time = time.time()
        # print("Check at {}".format(current_time - self.start_time))
        time_til_previous = self.start_time + (self.count * self.interval) - current_time
        if time_til_previous < 0:
            # print("Already got it {}".format(time_til_previous))
            ready = True
            wait_time = 0
        else:
            time_til_next = time_til_previous + self.interval
            if time_til_next <= timeout:
                ready = True
                wait_time = time_til_next
            else:
                ready = False
                wait_time = timeout
        # print("Ready {}, sleeping for {}".format(ready, wait_time))
        if wait_time > 0:
            time.sleep(wait_time)
        if ready:
            self.count += 1
        return ready
