import sys
import time

from rover_position_rjg.csv_helpers.csv_converter import CsvConverter
from rover_position_rjg.csv_helpers.csv_writer import CsvWriter
from rover_position_rjg.data.data import TValue, Data
from rover_position_rjg.data.data_filter import DataFilter


class ToCsvFilter(DataFilter[TValue, TValue]):
    """Records to a CSV file for a specified period of time."""

    def __init__(self, converter: CsvConverter[Data[TValue]], filename: str, duration: float = sys.float_info.max):
        super().__init__()
        self.duration = duration
        self.csv_writer = CsvWriter(filename, converter)
        self.csv_writer.open()
        self.start_time = time.time()

    def receive(self, data: Data[TValue]) -> None:
        if time.time() - self.start_time >= self.duration:
            self.close()
        if self.csv_writer:
            self.csv_writer.write(data)
        self.send(data)

    def close(self) -> None:
        if self.csv_writer:
            self.csv_writer.close()
            self.csv_writer = None
