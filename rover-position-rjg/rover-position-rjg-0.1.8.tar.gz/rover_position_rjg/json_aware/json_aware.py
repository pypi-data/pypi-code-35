from abc import *
from typing import Generic, TypeVar

TJsonAware = TypeVar('TJsonAware')


class JsonAware(Generic[TJsonAware], ABC):
    @abstractmethod
    def to_json(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def from_json(obj: dict) -> TJsonAware:
        pass
