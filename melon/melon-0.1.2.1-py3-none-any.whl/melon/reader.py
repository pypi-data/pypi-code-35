from abc import ABC, abstractmethod
from pathlib import Path


class Reader(ABC):

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def _validate_file(self, file):
        pass

    def _list_and_validate(self, source_dir):
        files = list(Path(source_dir).glob("*.*"))
        valid_files = []
        for file in files:
            if self._validate_file(file):
                valid_files.append(file)

        return valid_files
