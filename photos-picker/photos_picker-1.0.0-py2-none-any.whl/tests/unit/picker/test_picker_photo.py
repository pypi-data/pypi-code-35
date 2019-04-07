from unittest import TestCase
from mock import Mock
from mock import MagicMock  # noqa
import mock
from PIL.JpegImagePlugin import JpegImageFile
import unittest_dataprovider
from photospicker.picker.picker_photo import PickerPhoto


class TestPickerPhoto(TestCase):
    """Unit tests for PickerPhoto"""

    @mock.patch('PIL.Image.open')
    def test_retrieve_data_with_datetimeoriginal(self, image_open_mock):
        """
        Test retrieve_data when exif DateTimeOriginal is found

        :param MagicMock image_open_mock: mock for Image.open
        """
        img = Mock(spec=JpegImageFile)
        img._getexif.return_value = {36867: '2018-05-02 13:27:12'}
        image_open_mock.return_value = img

        sut = PickerPhoto('myfilepath')
        sut.retrieve_date()

        self.assertEqual('2018-05-02 13:27:12', sut._date)

    @staticmethod
    def provider_retrieve_date_without_datetimeoriginal():
        """
        Data provider test_retrieve_date_without_datetimeoriginal

        :return: tuple
        """
        mock2 = Mock(spec=JpegImageFile)
        mock2._getexif.return_value = None

        mock3 = Mock(spec=JpegImageFile)
        mock3._getexif.return_value = {36868: 'mydata'}

        return (
            (Mock(),),
            (mock2,),
            (mock3,)
        )

    @unittest_dataprovider.data_provider(
        provider_retrieve_date_without_datetimeoriginal
    )
    @mock.patch('PIL.Image.open')
    def test_retrieve_date_without_datetimeoriginal(
            self,
            img,
            image_open_mock
    ):
        """
        Test retrieve_data on different cases when DateTimeOriginal
        is not found

        :param MagicMock image_open_mock: mock for Image.open
        :param Mock img: mock returned by Image.open
        """
        image_open_mock.return_value = img

        sut = PickerPhoto('myfilepath')
        sut.retrieve_date()

        self.assertEqual('', sut._date)

    def test_date(self):
        """
        Test that date getter call retrieve_date once
        """
        get_datetimeoriginal_mock = Mock()
        get_datetimeoriginal_mock.return_value = '2018-07-13 12:23:31'

        sut = PickerPhoto('myfilepath')
        sut._get_datetimeoriginal = get_datetimeoriginal_mock
        self.assertEqual('2018-07-13 12:23:31', sut.date)
        self.assertEqual('2018-07-13 12:23:31', sut.date)

        get_datetimeoriginal_mock.assert_called_once()
