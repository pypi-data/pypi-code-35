from photospicker.picker.abstract_picker import AbstractPicker
from abc import ABCMeta, abstractmethod
import operator


class AbstractExifDatePicker(AbstractPicker):
    """Abstract class for pickers based on Exif photo date"""

    __metaclass__ = ABCMeta

    def _scan(self):  # pragma: no cover
        """
        Order photos by exif date and launch discriminating method

        :rtype: list
        """
        return self._select(self._build_photos_to_select_list())

    def _build_photos_to_select_list(self):
        """
        Create an ordered photos list to select photos inside

        :rtype: list
        """
        data_to_sort = []
        scanned = 0
        self._notify_progress(scanned)
        for picker_photo in self._files_to_scan:
            date = picker_photo.date
            if date:
                data_to_sort.append(picker_photo)

            scanned += 1
            self._notify_progress(scanned)

        self._notify_end()

        return sorted(
            data_to_sort,
            key=operator.attrgetter('date'),
            reverse=True
        )

    @abstractmethod
    def _select(self, to_select):  # pragma: no cover
        """
        Finally select photos

        :param list to_select: list where process selection

        :rtype: list
        """
        raise NotImplementedError()
