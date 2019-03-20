import csv
from typing import Generic

from rover_position_rjg.csv_helpers.csv_converter import CsvConverter, TObject


class CsvWriter(Generic[TObject]):

    def __init__(self, filename: str, converter: CsvConverter[TObject]) -> None:
        self.filename = filename
        self.converter = converter

    def __enter__(self):
        self.file = open(self.filename, 'w')
        self.writer = csv.writer(self.file, lineterminator='\n')
        return self

    def open(self):
        self.__enter__()

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        self.file.close()
        self.file = None
        return False

    def close(self):
        self.__exit__(None, None, None)

    def write(self, something: TObject) -> None:
        row = self.converter.to_row(something)
        self.writer.writerow(row)


