from photospicker.picker.abstract_exif_date_picker import \
    AbstractExifDatePicker


class LastPhotosPicker(AbstractExifDatePicker):
    """Pick the lastest photos by DateTimeOriginal in EXIF data"""

    def _select(self, to_select):
        """
        Finally select photos

        :param list to_select: list where process selection

        :rtype: list
        """
        return [
            filename for key, filename in enumerate(to_select)
            if key < self._photos_count
        ]
