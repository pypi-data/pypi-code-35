from photospicker.filter.abstract_filter import AbstractFilter
from PIL import Image


class ResizeFilter(AbstractFilter):
    """Resize a photo"""

    def __init__(self, max_width, max_height):
        """
        Constructor

        :param int max_width : max width after filter execution
        :param int max_height: max height after filter execution
        """
        self._width = float(max_width)
        self._height = float(max_height)

    def execute(self, original_img, exif_data):
        """
        Resize photo

        :param Image original_img: image object to resize
        :param dict exif_data    : image exif data

        :rtype: Image
        """
        (original_width_int, original_height_int) = original_img.size
        original_width = float(original_width_int)
        original_height = float(original_height_int)

        if original_width / original_height > self._width / self._height:
            ratio = self._width / original_width
        else:
            ratio = self._height / original_height

        resized_img = original_img.resize(
            (int(ratio * original_width), int(ratio * original_height)),
            Image.ANTIALIAS
        )

        return resized_img
