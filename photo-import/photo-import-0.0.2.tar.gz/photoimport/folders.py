import os
import shutil


class FolderCreator:

    def __init__(self, base_dir):
        self._base_dir = base_dir

    def create_folder(self, date):
        path = self._build_path(date)
        os.makedirs(path, exist_ok=True)

    def move_file(self, file, date):
        shutil.move(file, self._build_path(date))

    def _build_path(self, date):
        year = '{:04d}'.format(date.year)
        month = '{:02d}'.format(date.month)
        day = '{:02d}'.format(date.day)
        path = os.path.join(self._base_dir, year, month, day)
        return path
