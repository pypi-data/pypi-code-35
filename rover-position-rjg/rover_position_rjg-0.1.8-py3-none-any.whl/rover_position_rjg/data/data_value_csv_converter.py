import time

from rover_position_rjg.data.data import *
from rover_position_rjg.csv_helpers.csv_converter import *


class DataValueCsvConverter(CsvConverter[Data[TValue]]):
    """Delegates work to another converter which doesn't know about Data[]"""

    def __init__(self, converter: CsvConverter[TValue]):
        self.converter = converter

    def to_object(self, row: Iterable[TCsvItem]) -> Data[TValue]:
        value = self.converter.to_object(row)
        return Data(value, time.time())

    def to_row(self, value: Data[TValue]) -> Iterable[TCsvItem]:
        return self.converter.to_row(value.value)
