from abc import ABC, abstractmethod
from os.path import exists, join
from typing import List


class AbstractDataset(ABC):
    destination_dir = None
    extracted_files = []

    @abstractmethod
    def download_to_dir(self, destination_dir: str) -> bool:
        """
        download all the files to the destination_dir if not exists
        Args:
            destination_dir: local destination directory, toplevel_datadir/dataset_name

        Returns:
            indicates if download is successful
        """
        pass

    def download_if_not_exists(self, destination_dir: str) -> bool:
        """
        download all the files to the destination_dir if not exists
        Args:
            destination_dir: local destination directory, toplevel_datadir/dataset_name

        Returns:
            indicates if download is successful
        """
        if self._check_if_exist_all(self.extracted_files):
            print("All files are already downloaded")
            return True

        return self.download_to_dir(destination_dir)

    def _check_if_exist_all(self, extracted_files: List[str]) -> bool:
        """
        check if all the files already extracted and exists
        Args:
            extracted_files: list of file path under destination_dir

        Returns:
            indicates if need to download or extract
        """

        for file in extracted_files:
            if not exists(join(self.destination_dir, file)):
                return False

        return True
