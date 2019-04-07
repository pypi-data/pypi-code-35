from unittest import TestCase

from photospicker.picker.picker_photo import PickerPhoto
from photospicker.picker.pickers.random_picker import RandomPicker
from mock import MagicMock  # noqa
import mock
from mock import Mock

from tests.unit.picker.picker_photo_stub import PickerPhotoStub


class TestRandomPicker(TestCase):
    """Test class for RandomPicker"""

    @mock.patch('random.shuffle')
    @mock.patch('os.walk')
    def test_scan(self, walk_mock, shuffle_mock):
        """
        Test random pick

        :param MagicMock walk_mock   : mock for os.walk
        :param MagicMock shuffle_mock: mock for random.shuffle
        """
        walk_mock.return_value = [['', [], [
            'myphoto1.jpg',
            'myphoto2.jpg',
            'myphoto3.jpg',
            'myphoto4.jpg'
        ]]]

        shuffle_mock.side_effect = self._shuffle_mock_side_effect
        order_picked_mock = Mock()
        order_picked_mock.side_effect = self._order_picked_side_effect

        sut = RandomPicker('', 2)
        sut._order_picked = order_picked_mock
        sut.initialize()
        sut.scan()

        shuffle_mock.assert_called_once_with([
            PickerPhotoStub('myphoto3.jpg'),
            PickerPhotoStub('myphoto2.jpg'),
            PickerPhotoStub('myphoto4.jpg'),
            PickerPhotoStub('myphoto1.jpg')
        ])

        self.assertEqual(
            ['myphoto3.jpg', 'myphoto2.jpg'],
            sut.picked_file_paths
        )

    def _shuffle_mock_side_effect(self, files):
        """
        Side effect for shuffle mock

        :param list files: file list
        """

        self.assertEqual(files, [
            PickerPhotoStub('myphoto1.jpg'),
            PickerPhotoStub('myphoto2.jpg'),
            PickerPhotoStub('myphoto3.jpg'),
            PickerPhotoStub('myphoto4.jpg')
        ])

        del files[:]
        files.append(PickerPhoto('myphoto3.jpg'))
        files.append(PickerPhoto('myphoto2.jpg'))
        files.append(PickerPhoto('myphoto4.jpg'))
        files.append(PickerPhoto('myphoto1.jpg'))

    @staticmethod
    def _order_picked_side_effect(to_order):
        """
        Identity side effect for __order_picked

        :param list to_order: list to order

        :return: list
        """
        return to_order
