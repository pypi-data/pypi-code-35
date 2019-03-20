from typing import Iterable

from decawave_1001_rjg import DwmLocationResponse

from rover_position_rjg.csv_helpers.csv_converter import CsvConverter, TCsvItem
from rover_position_rjg.sensors.decawave.csv.dwm_distance_and_position_to_csv import DwmDistanceAndPositionCsvConverter
from rover_position_rjg.sensors.decawave.csv.dwm_position_to_csv import DwmPositionCsvConverter


class DwmLocationResponseCsvConverter(CsvConverter[DwmLocationResponse]):
    def __init__(self):
        self.position_converter = DwmPositionCsvConverter()
        self.dp_converter = DwmDistanceAndPositionCsvConverter()

    def to_row(self, value: DwmLocationResponse) -> Iterable[TCsvItem]:
        data = self.position_converter.to_row(value.get_tag_position())
        for dp in value.get_anchor_distances_and_positions():
            data = data + self.dp_converter.to_row(dp)
        return data

    def to_object(self, row: Iterable[TCsvItem]) -> DwmLocationResponse:
        r = list(row)
        tag_position = self.position_converter.to_object(row[0:4])
        anchors_offset = 4
        anchor_length = 7
        num_anchors = int((len(r) - anchors_offset) / anchor_length)
        anchors = []
        for i in range(0, num_anchors):
            start = anchors_offset + i * anchor_length
            dp_row = r[start: start + anchor_length]
            built_dp = self.dp_converter.to_object(dp_row)
            anchors.append(built_dp)
        return DwmLocationResponse.from_properties(tag_position, anchors)
