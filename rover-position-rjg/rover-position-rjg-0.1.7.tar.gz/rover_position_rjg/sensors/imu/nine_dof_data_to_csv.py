from typing import Iterable

from rover_position_rjg.csv_helpers.csv_converter import CsvConverter, TCsvItem
from rover_position_rjg.data.data import Data
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class NineDoFDataCsvConverter(CsvConverter[NineDoFData]):
    def to_object(self, row: Iterable[TCsvItem]) -> NineDoFData:
        values = list(row)
        acceleration = self._parse_vector(values[0:4])
        angular_velocity = self._parse_vector(values[4:8])
        magnetic_field = self._parse_vector(values[8:12])
        temperature = self._parse_temp(values[12:14])
        return NineDoFData(acceleration, angular_velocity, magnetic_field, temperature)

    def to_row(self, value: NineDoFData) -> Iterable:
        return self._write_vector(value.acceleration) + \
               self._write_vector(value.angular_velocity) + \
               self._write_vector(value.magnetic_field) + \
               self._write_temp(value.temperature)

    @staticmethod
    def _parse_vector(values: list) -> Data[Vector]:
        x = values[0]
        y = values[1]
        z = values[2]
        time = values[3]
        value = None
        if x is not None or y is not None or z is not None:
            value = Vector([x, y, z])
        if value or time:
            return Data[Vector](value, time)

    @staticmethod
    def _write_vector(data: Data[Vector]):
        if not data:
            return [None, None, None, None]
        value = data.value
        if not value:
            return [None, None, None, data.timestamp]
        return [value.x, value.y, value.z, data.timestamp]

    @staticmethod
    def _parse_temp(values: list) -> Data[float]:
        temp = values[0]
        time = values[1]
        if temp or time:
            return Data[float](values[0], values[1])

    @staticmethod
    def _write_temp(data: Data):
        if not data:
            return [None, None]
        return [data.value, data.timestamp]
