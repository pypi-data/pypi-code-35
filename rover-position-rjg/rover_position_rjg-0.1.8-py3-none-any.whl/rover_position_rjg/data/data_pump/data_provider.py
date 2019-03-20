from abc import *
from rover_position_rjg.data.data import *


class DataProvider(Generic[TValue], ABC):
    """Supplies data from some source or other. e.g. a file./
    Unlike DataPump, the provider blocks while reading data.
    """

    @abstractmethod
    def get(self) -> Data[TValue]:
        """Returns the next piece of data"""
        pass

    @abstractmethod
    def poll(self, timeout: float) -> bool:
        """
        Waits efficiently until data is available or the timeout
        period has passed
        :param timeout: maximum time to wait in seconds
        :returns True if data is available. False if it timed out.
        """
        pass

    @abstractmethod
    def close(self):
        """Tidy up any resources"""
        pass
