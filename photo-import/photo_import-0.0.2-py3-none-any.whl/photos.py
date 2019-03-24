import os
from datetime import datetime

from exif import Image


class ExifReader:

    def __init__(self, base_dir):
        self._base_dir = base_dir

    def extract_date(self, filename):
        path = os.path.join(self._base_dir, filename)
        with open(path, 'rb') as image_file:
            image = Image(image_file)
            return datetime.strptime(image.datetime_original, '%Y:%m:%d %H:%M:%S').date()
