from abc import ABCMeta, abstractmethod
from photospicker.event.scan_progress_event import ScanProgressEvent
from zope import event
from photospicker.exception.picker_exception import PickerException
import os
import fnmatch
import random
import operator
from photospicker.picker.picker_photo import PickerPhoto


class AbstractPicker:
    """
    Abstract class for creating "picker" classes

    A picker object select files in a path according to a strategy
    which characterizes the picker
    """

    __metaclass__ = ABCMeta

    def __init__(
            self,
            directory_paths,
            photos_count,
            order=0,
            patterns=None,
            excluded_patterns=None
    ):
        """
        Constructor

        :param mixed directory_paths: directory paths to scan
        :param int photos_count: photos count to pick
        :param int order: 0 for random order
                          -1 for order from newer to older
                          1 for order from older to newer
        :param list patterns: patterns (in lowercase) that files must match
                              for being scanned
        :param list excluded_patterns: directory patterns excluded
                                       form the scan

        :raise TypeError
        """
        if isinstance(directory_paths, list):
            self._paths = directory_paths
        else:
            self._paths = [directory_paths]

        self._order = order
        self._files_to_scan = []
        self._picked_file_paths = []
        self._photos_count = photos_count

        if patterns is None:
            patterns = ['*.tif', '*.tiff', '*.jpg', '*.jpeg', '*.png']
        elif not isinstance(patterns, list):
            raise TypeError("patterns argument must be a list")

        self._patterns = patterns

        if excluded_patterns is None:
            self._excluded_patterns = []
        else:
            self._excluded_patterns = excluded_patterns

    @property
    def picked_file_paths(self):
        """Return an array of the picked file paths"""
        return self._picked_file_paths

    def initialize(self):
        """Fill in the list of files to scan"""
        for path in self._paths:
            for root, dirnames, filenames in os.walk(os.path.expanduser(path)):
                if self._is_in_excluded_patterns(root):
                    continue
                for filename in filenames:
                    for pattern in self._patterns:
                        if fnmatch.fnmatch(filename.lower(), pattern):
                            self._files_to_scan.append(PickerPhoto(
                                os.path.join(root, filename)
                            ))
        if not self._files_to_scan:
            raise PickerException(
                PickerException.EMPTY_SCAN,
                "No photos to scan found in given directory(ies)"
            )
        files_to_scan_len = len(self._files_to_scan)
        if self._photos_count > files_to_scan_len:
            self._photos_count = files_to_scan_len

    def _is_in_excluded_patterns(self, path):
        """
        Check if a path match with an excluded pattern

        :param string path: path to check

        :rtype: bool
        """
        for excluded_pattern in self._excluded_patterns:
            expandeduser_pattern = os.path.expanduser(excluded_pattern)
            if (path + '/').find(expandeduser_pattern) != -1:
                return True
        return False

    @abstractmethod
    def _scan(self):  # pragma: no cover
        """
        Scan the given path and return picked file paths list

        :rtype: list

        :raise NotImplementedError
        """
        raise NotImplementedError()

    def scan(self):
        """Scan the given path for building picked file paths list"""
        picker_photos = self._order_picked(self._scan())
        self._picked_file_paths = [
            picker_photo.filepath for picker_photo in picker_photos
        ]

    def _order_picked(self, picked):
        """
        Order picked files

        :param list picked: list of PickerPhoto previously picked

        :rtype: list
        """
        if self._order == 0:
            random.shuffle(picked)
        else:
            picked = sorted(
                picked,
                key=operator.attrgetter('date'),
                reverse=self._order < 0
            )

        return picked

    def _notify_progress(self, scanned):
        """
        Notify the progress state of the scan

        :param int scanned: scanned files count
        """
        event.notify(ScanProgressEvent(
            scanned,
            len(self._files_to_scan),
            False
        ))

    def _notify_end(self):
        """Notify the end of the scan"""
        to_scan = len(self._files_to_scan)
        event.notify(ScanProgressEvent(to_scan, to_scan, True))
