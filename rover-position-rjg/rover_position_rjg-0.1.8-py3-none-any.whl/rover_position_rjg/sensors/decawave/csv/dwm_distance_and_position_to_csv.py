from typing import Iterable

from decawave_1001_rjg import DwmDistanceAndPosition

from rover_position_rjg.csv_helpers.csv_converter import CsvConverter, TCsvItem
from rover_position_rjg.sensors.decawave.csv.dwm_position_to_csv import DwmPositionCsvConverter


class DwmDistanceAndPositionCsvConverter(CsvConverter[DwmDistanceAndPosition]):
    def __init__(self):
        self.position_converter = DwmPositionCsvConverter()

    def to_row(self, value: DwmDistanceAndPosition) -> Iterable[TCsvItem]:
        result = [value.address(),
                  value.distance(),
                  value.quality_factor()]
        return result + list(self.position_converter.to_row(value.position()))

    def to_object(self, row: Iterable[TCsvItem]) -> DwmDistanceAndPosition:
        r = list(row)
        position = self.position_converter.to_object(r[3:])
        address = str.strip(r[0])
        if len(address) == 6:
            address = address[1:5]
        return DwmDistanceAndPosition.from_properties(address, int(r[1]), int(r[2]), position)
