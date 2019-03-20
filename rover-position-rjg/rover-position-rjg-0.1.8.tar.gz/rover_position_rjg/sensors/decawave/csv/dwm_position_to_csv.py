from typing import Iterable

from decawave_1001_rjg import DwmPosition

from rover_position_rjg.csv_helpers.csv_converter import CsvConverter, TCsvItem
from rover_position_rjg.csv_helpers.vector_csv_converter import VectorCsvConverter


class DwmPositionCsvConverter(CsvConverter[DwmPosition]):
    def __init__(self):
        self.vector_converter = VectorCsvConverter()

    def to_row(self, value: DwmPosition) -> Iterable[TCsvItem]:
        result = value.position()
        result.append(value.quality_factor())
        return result

    def to_object(self, row: Iterable[TCsvItem]) -> DwmPosition:
        the_row = []
        for value in row:
            the_row.append(int(value))
        position = the_row[0:3]
        return DwmPosition.from_properties(position, the_row[3])
