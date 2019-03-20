from abc import *
from typing import TypeVar, Generic, Iterable

TObject = TypeVar('TObject')
TCsvItem = TypeVar('TCsvItem', str, int, float)


class CsvConverter(Generic[TObject], ABC):
    """Converts some sort of object to and from a CSV row"""

    @abstractmethod
    def to_row(self, value: TObject) -> Iterable[TCsvItem]:
        """Converts an object into a row.
        :return an iterable of strings or numbers
        """
        pass

    @abstractmethod
    def to_object(self, row: Iterable[TCsvItem]) -> TObject:
        """Converts a CSV row into an object
        :return an object
        """
        pass
