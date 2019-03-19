from typing import Iterable

from rover_position_rjg.csv_helpers.csv_converter import CsvConverter, TCsvItem
from rover_position_rjg.data.vector import Vector


class VectorCsvConverter(CsvConverter[Vector]):
    def to_row(self, value: Vector) -> Iterable[TCsvItem]:
        return value.values

    def to_object(self, row: Iterable[TCsvItem]) -> Vector:
        r = list(row)
        return Vector([float(r[0]), float(r[1]), float(r[2])])
