from PIL import Image, ExifTags
from PIL.JpegImagePlugin import JpegImageFile


class PickerPhoto(object):
    """Photo object for pickers usage"""

    def __init__(self, filepath):
        """
        Constructor

        :param str filepath: filepath
        """
        self._filepath = filepath
        self._date = None

    def retrieve_date(self):
        """
        Retrieve date and store it
        """
        self._date = self._get_datetimeoriginal()

    def _get_datetimeoriginal(self):
        """
        Return exif DateTimeOriginal

        :rtype: str
        """
        img = Image.open(self._filepath)
        if isinstance(img, JpegImageFile):
            exif_data = img._getexif()

            if exif_data is None:
                exif_data = {}

            for key in exif_data.keys():
                if ExifTags.TAGS.get(key) == 'DateTimeOriginal':
                    return exif_data[key]
        return ''

    @property
    def filepath(self):
        """
        Getter for _filepath

        :rtype: str
        """
        return self._filepath

    @property
    def date(self):
        """
        Getter for _date (exif date)

        :rtype: str
        """
        if self._date is None:
            self.retrieve_date()

        return self._date
