from abc import ABC, abstractmethod
from typing import Generic

from rover_position_rjg.data.data import Data, TValue


class Scaler(Generic[TValue], ABC):
    """Scales data in some fashion"""

    @abstractmethod
    def scale(self, data: Data[TValue]) -> Data[TValue]:
        """Returns a scaled version of the value"""
        pass
