from photospicker.picker.picker_photo import PickerPhoto
from photospicker.picker.pickers.last_photos_picker import LastPhotosPicker
from unittest import TestCase
from mock import Mock


class TestLastPhotosPicker(TestCase):
    """Test class for LastPhotosPicker"""

    def test_scan(self,):
        """Test scan method"""

        order_picked_mock = Mock()
        order_picked_mock.side_effect = self._order_picked_side_effect

        sut = LastPhotosPicker('', 2)
        sut._order_picked = order_picked_mock
        build_method_mock = Mock()
        build_method_mock.return_value = [
            PickerPhoto('myphoto4.jpg'),
            PickerPhoto('myphoto1.jpg'),
            PickerPhoto('myphoto3.jpg')
        ]
        sut._build_photos_to_select_list = build_method_mock
        sut.scan()

        self.assertEqual(
            ['myphoto4.jpg', 'myphoto1.jpg'],
            sut.picked_file_paths
        )

    @staticmethod
    def _order_picked_side_effect(to_order):
        """
        Identity side effect for __order_picked

        :param list to_order: list to order

        :return: list
        """
        return to_order
