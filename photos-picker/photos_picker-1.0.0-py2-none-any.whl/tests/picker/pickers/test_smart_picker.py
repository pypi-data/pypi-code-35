from unittest import TestCase
from mock import Mock
from mock import MagicMock  # noqa
from photospicker.picker.picker_photo import PickerPhoto
from photospicker.picker.pickers.smart_picker import SmartPicker
import mock
import unittest_dataprovider

from tests.picker.picker_photo_stub import PickerPhotoStub


class TestSmartPicker(TestCase):
    """Test class for SmartPicker"""

    @staticmethod
    def provider_scan():
        return (
            (
                100,
                15,
                [7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 92, 100],
                [1, 2, 8, 15, 22, 29, 36, 43, 50, 57, 64, 71, 78, 85, 93]
            ),
            (
                50,
                20,
                [
                    2, 5, 8, 11, 14, 17, 20, 23, 26,
                    29, 32, 35, 38, 41, 44, 47, 50
                ],
                [
                    1, 2, 3, 4, 6, 7, 9, 12, 15, 18, 21,
                    24, 27, 30, 33, 36, 39, 42, 45, 48
                ]
            ),
            (
                120,
                80,
                [120],
                range(1, 81)
            ),
            (
                100,
                100,
                [100],
                range(1, 101)
            )
        )

    @unittest_dataprovider.data_provider(provider_scan)
    @mock.patch('random.shuffle')
    def test_scan(
            self,
            photos_count,
            photos_to_retrieve,
            calls_data,
            expected_indexes,
            shuffle_mock
    ):
        """
        Test scan method

        :param int photos_count: photos count for the test
        :param int photos_to_retrieve: photos to retrieve count
        :param list calls_data: data for building expected shuffle call list
        :param list expected_indexes: indexes of the exoected picked photos
        :param MagicMock shuffle_mock: mock for random.shuffle
        """

        shuffle_mock.side_effect = self._shuffle_mock_side_effect

        sut = SmartPicker('', photos_to_retrieve)
        filenames_returned = []
        for i in range(1, photos_count + 1):
            filenames_returned.append(
                PickerPhoto('myphoto{i}.jpg'.format(i=i))
            )

        build_method_mock = Mock()
        build_method_mock.return_value = filenames_returned
        sut._build_photos_to_select_list = build_method_mock
        sut.scan()

        i = 0
        call = []
        calls = []
        while len(calls_data):
            i += 1
            call.append(PickerPhotoStub('myphoto{i}.jpg'.format(i=i)))
            if i == calls_data[0]:
                calls.append(mock.call(call))
                call = []
                calls_data.pop(0)

        shuffle_mock.assert_has_calls(calls)

        expected_picked = []
        for i in expected_indexes:
            expected_picked.append('myphoto{i}.jpg'.format(i=i))

        self.assertEqual(
            expected_picked,
            sut.picked_file_paths
        )

    @staticmethod
    def _shuffle_mock_side_effect(photos):
        """
        Side effect for shuffle mock

        :param list photos: photo paths

        :return: list
        """
        return photos
