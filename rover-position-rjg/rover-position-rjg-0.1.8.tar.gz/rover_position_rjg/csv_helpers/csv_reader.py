import csv
from typing import Iterator, Generic, Iterable
from rover_position_rjg.csv_helpers.csv_converter import CsvConverter, TObject


class CsvReader(Generic[TObject], Iterator[TObject], Iterable[TObject]):

    def __init__(self, filename: str, converter: CsvConverter[TObject]) -> None:
        self.filename = filename
        self.converter = converter

    def __enter__(self):
        self.file = open(self.filename)
        self.reader = csv.reader(self.file)
        self.reader_iter = self.reader.__iter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        self.file.close()
        self.file = None
        return False

    def __iter__(self) -> Iterator[TObject]:
        return self

    def __next__(self) -> TObject:
        row = self.reader_iter.__next__()
        result = self.converter.to_object(row)
        return result
