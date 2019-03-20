from abc import *
from rover_position_rjg.data.data import *


class DataPump(Generic[TValue], ABC):
    """Supplies data from some source or other. e.g. polling sensors"""

    @abstractmethod
    def poll(self, timeout: float) -> bool:
        """Waits for timeout seconds to see if there is data available.
        :param timeout: maximum time to wait in seconds
        :return true if there is data available
        """
        pass

    @abstractmethod
    def recv(self) -> Data[TValue]:
        """Gets the next available piece of data from the pump. Throws an exception if there's nothing ready."""
        pass

    @abstractmethod
    def run(self):
        """Start pumping"""
        pass

    @abstractmethod
    def halt(self):
        """Stop pumping"""
        pass

    @abstractmethod
    def pause(self):
        """Pause pumping. The pump enters a low power state and ignores all new data.
        Call resume() to start pumping again. Ignored if already paused."""
        pass

    @abstractmethod
    def resume(self):
        """Resumes pumping after pause(). Ignored if already resumed."""
        pass

    @abstractmethod
    def fileno(self) -> int:
        """Returns a file handle for use by multiprocessing.connection.wait()"""
        pass

    @property
    @abstractmethod
    def name(self):
        return