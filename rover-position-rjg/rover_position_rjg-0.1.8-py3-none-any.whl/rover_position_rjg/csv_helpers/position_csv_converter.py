from typing import Iterable

from rover_position_rjg.csv_helpers.csv_converter import CsvConverter, TCsvItem
from rover_position_rjg.csv_helpers.quaternion_csv_converter import QuaternionCsvConverter
from rover_position_rjg.csv_helpers.vector_csv_converter import VectorCsvConverter
from rover_position_rjg.position.position.position import Position


class PositionCsvConverter(CsvConverter[Position]):
    def __init__(self):
        self.vector_converter = VectorCsvConverter()
        self.quaternion_converter = QuaternionCsvConverter()

    def to_row(self, value: Position) -> Iterable[TCsvItem]:
        if value.attitude:
            result = list(self.quaternion_converter.to_row(value.attitude))
        else:
            result = [None, None, None, None]
        result.extend(self.vector_converter.to_row(value.acceleration))
        result.extend(self.vector_converter.to_row(value.velocity))
        result.extend(self.vector_converter.to_row(value.position))
        return result

    def to_object(self, row: Iterable[TCsvItem]) -> Position:
        attitude_data = row[0:4]
        if attitude_data == [None, None, None, None]:
            attitude = None
        else:
            attitude = self.quaternion_converter.to_object(attitude_data)
        acceleration = self.vector_converter.to_object(row[4:7])
        velocity = self.vector_converter.to_object(row[7:10])
        position = self.vector_converter.to_object(row[10:13])
        return Position(attitude, acceleration, velocity, position)
