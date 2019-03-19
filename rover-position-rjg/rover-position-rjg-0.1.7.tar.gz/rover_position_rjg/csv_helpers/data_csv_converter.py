from typing import Iterable

from rover_position_rjg.csv_helpers.csv_converter import CsvConverter, TCsvItem
from rover_position_rjg.data.data import Data, TValue


class DataCsvConverter(CsvConverter[Data[TValue]]):
    def __init__(self, value_converter: CsvConverter[TValue]):
        self.value_converter = value_converter

    def to_row(self, value: Data[TValue]) -> Iterable[TCsvItem]:
        row = list(self.value_converter.to_row(value.value))
        row.append(value.timestamp)
        return row

    def to_object(self, row: Iterable[TCsvItem]) -> Data[TValue]:
        row = list(row)
        timestamp = float(row.pop(len(row)-1))
        value = self.value_converter.to_object(row)
        return Data(value, timestamp)
