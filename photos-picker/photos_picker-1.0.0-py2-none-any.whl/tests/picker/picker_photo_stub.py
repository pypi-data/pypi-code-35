from photospicker.picker.picker_photo import PickerPhoto


class PickerPhotoStub(PickerPhoto):
    """Stub for comparing with PickerPhoto objects"""
    def __init__(self, filepath, date=None):
        """
        Constructor

        :param str filepath: filepath
        :param str date: exif date
        """
        super(PickerPhotoStub, self).__init__(filepath)
        self._date = date

    def __eq__(self, other):
        """Equality behavior"""
        if not isinstance(other, PickerPhoto):
            return False

        return self._filepath == other._filepath and self._date == self._date
