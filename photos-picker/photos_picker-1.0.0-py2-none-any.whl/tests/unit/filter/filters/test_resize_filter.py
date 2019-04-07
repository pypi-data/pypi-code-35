from unittest import TestCase
from photospicker.filter.filters.resize_filter import ResizeFilter
from PIL import Image
from mock import Mock
import unittest_dataprovider


class TestResizeFilter(TestCase):
    """Unit tests for ResizeFilter"""

    @staticmethod
    def provider_execute():
        """
        Data provider for test_execute

        :return: tuple
        """
        return (
            ((300, 150), (20, 20), (20, 10)),
            ((300, 150), (20, 30), (20, 10)),
            ((300, 150), (20, 60), (20, 10)),
            ((300, 150), (30, 20), (30, 15)),
            ((300, 150), (60, 20), (40, 20)),
            ((300, 150), (60, 60), (60, 30)),

            ((300, 300), (20, 20), (20, 20)),
            ((300, 300), (20, 30), (20, 20)),
            ((300, 300), (20, 60), (20, 20)),
            ((300, 300), (30, 20), (20, 20)),
            ((300, 300), (60, 20), (20, 20)),
            ((300, 300), (60, 60), (60, 60)),

            ((150, 300), (20, 20), (10, 20)),
            ((150, 300), (20, 30), (15, 30)),
            ((150, 300), (20, 60), (20, 40)),
            ((150, 300), (30, 20), (10, 20)),
            ((150, 300), (60, 20), (10, 20)),
            ((150, 300), (60, 60), (30, 60)),
        )

    @unittest_dataprovider.data_provider(provider_execute)
    def test_execute(self, img_size, filter_size, expected_img_size):
        """
        Test execute method

        :param tuple img_size: original imgage size
        :param tuple filter_size: parameterized size of the filter
        :param tuple expected_img_size: expected size of the returned image
        """
        original_img = Mock()
        original_img.size = img_size
        original_img.format = 'JPEG'

        resized_mock = Mock()
        original_img.resize.return_value = resized_mock

        sut = ResizeFilter(filter_size[0], filter_size[1])
        resized_img = sut.execute(original_img, 'myexifdata')

        original_img.resize.assert_called_once_with(
            (expected_img_size[0], expected_img_size[1]),
            Image.ANTIALIAS
        )

        self.assertEqual(resized_mock, resized_img)
