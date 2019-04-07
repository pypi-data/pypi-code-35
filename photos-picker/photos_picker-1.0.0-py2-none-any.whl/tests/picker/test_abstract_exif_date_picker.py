from PIL.JpegImagePlugin import JpegImageFile
from unittest import TestCase
from photospicker.picker.abstract_exif_date_picker import \
    AbstractExifDatePicker
from mock import MagicMock  # noqa
from mock import Mock
import mock

from photospicker.picker.picker_photo import PickerPhoto
from tests.picker.picker_photo_stub import PickerPhotoStub


class DummyPicker(AbstractExifDatePicker):
    """Dummy class for testing AbstractExifDatePicker"""

    def _select(self):
        """Dummy abstract method"""
        pass


class TestAbstractExifDatePicker(TestCase):
    """Unit tests for AbstractExifDatePicker"""

    @mock.patch('PIL.Image.open')
    @mock.patch('os.walk')
    def test_select(self, walk_mock, image_open_mock):
        """
        Test select

        :param MagicMock walk_mock:       mock for walk method
        :param MagicMock image_open_mock: mock for PIL Image mock method
        """

        walk_mock.return_value = [['', [], [
            'myphoto1.jpg',
            'myphoto2.jpg',
            'myphoto3.jpg',
            'myphoto4.jpg',
            'myphoto5.jpg'
        ]]]

        image_mock1 = Mock(spec=JpegImageFile)
        image_mock1._getexif.return_value = {
            36865: 'myData',
            36867: '2017-05-01 23:50:00'
        }

        image_mock2 = Mock(spec=JpegImageFile)
        image_mock2._getexif.return_value = None

        image_mock3 = Mock(spec=JpegImageFile)
        image_mock3._getexif.return_value = {
            36867: '2017-05-01 23:49:50',
            36882: 'myOtherData'
        }

        image_mock4 = Mock(spec=JpegImageFile)
        image_mock4._getexif.return_value = {
            36864: 'myOtherData',
            36867: '2017-05-01 23:55:00',
            36888: 'anotherData'
        }

        image_mock5 = Mock()

        image_open_mock.side_effect = [
            image_mock1,
            image_mock2,
            image_mock3,
            image_mock4,
            image_mock5
        ]

        expected_ordered = [
            PickerPhotoStub('myphoto4.jpg'),
            PickerPhotoStub('myphoto1.jpg'),
            PickerPhotoStub('myphoto3.jpg')
        ]
        expected_selected = [
            'myphoto4.jpg',
            'myphoto1.jpg'
        ]

        select_mock = Mock()
        select_mock.return_value = [
            PickerPhoto(filepath) for filepath in expected_selected
        ]

        order_picked_mock = Mock()
        order_picked_mock.side_effect = self._order_picked_side_effect

        sut = DummyPicker('', 0)
        sut._select = select_mock
        sut._order_picked = order_picked_mock
        sut.initialize()
        sut.scan()

        select_mock.assert_called_once_with(
            expected_ordered
        )

        self.assertEqual(expected_selected, sut.picked_file_paths)

    @staticmethod
    def _order_picked_side_effect(to_order):
        """
        Identity side effect for __order_picked

        :param list to_order: list to order

        :return: list
        """
        return to_order
