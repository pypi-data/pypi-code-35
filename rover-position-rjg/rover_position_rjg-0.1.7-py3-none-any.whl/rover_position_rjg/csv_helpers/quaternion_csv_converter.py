from typing import Iterable

from rover_position_rjg.csv_helpers.csv_converter import CsvConverter, TCsvItem
from rover_position_rjg.data.quaternion import Quaternion


class QuaternionCsvConverter(CsvConverter[Quaternion]):
    def to_row(self, value: Quaternion) -> Iterable[TCsvItem]:
        return [value.w, value.i, value.j, value.k]

    def to_object(self, row: Iterable[TCsvItem]) -> Quaternion:
        r = list(row)
        return Quaternion(r[0], r[1], r[2], r[3])
