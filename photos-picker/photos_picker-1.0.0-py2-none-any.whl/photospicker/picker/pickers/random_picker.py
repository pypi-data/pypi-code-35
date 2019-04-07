from photospicker.picker.abstract_picker import AbstractPicker
import random


class RandomPicker(AbstractPicker):
    """Pick photos randomly"""

    def _scan(self):
        """
        Scan the given path and return picked file paths list

        :rtype: list
        """
        self._notify_progress(0)
        random.shuffle(self._files_to_scan)
        self._notify_progress(len(self._files_to_scan))
        self._notify_end()

        return self._files_to_scan[0:self._photos_count]
