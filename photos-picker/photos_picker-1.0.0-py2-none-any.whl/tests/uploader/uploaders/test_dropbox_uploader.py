from unittest import TestCase

from photospicker.exception.uploader_exception import UploaderException
from photospicker.uploader.uploaders.dropbox_uploader import DropboxUploader
from mock import Mock
from mock import MagicMock  # noqa
from dropbox.exceptions import ApiError
from dropbox.files import LookupError
from dropbox.files import DeleteError
import mock


class TestDropboxUploader(TestCase):
    """Test class for DropboxUploader"""

    @mock.patch('photospicker.uploader.uploaders.dropbox_uploader.Dropbox')
    def test_initialize(self, dropbox_constructor_mock):
        """
        Test initialize

        :param MagicMock dropbox_constructor_mock:
                                                mock for dropbox constructor
        """
        dropbox_mock = Mock()
        dropbox_constructor_mock.return_value = dropbox_mock

        dropbox_uploader = DropboxUploader(None, 'my-customer-dir')
        dropbox_uploader.initialize()

        dropbox_mock.files_delete_v2.assert_called_once_with(
            '/my-customer-dir'
        )

    @mock.patch('photospicker.uploader.uploaders.dropbox_uploader.Dropbox')
    def test_upload(self, dropbox_constructor_mock):
        """
        Test upload

        :param MagicMock dropbox_constructor_mock:
                                                mock for dropbox constructor
        """

        dropbox_mock = Mock()
        dropbox_constructor_mock.return_value = dropbox_mock

        dropbox_uploader = DropboxUploader('mytoken', 'my-customer-dir')
        dropbox_uploader.increase_photo_counter()
        dropbox_uploader.upload('mybinarydata', 'myphoto.png')
        dropbox_uploader.increase_photo_counter()
        dropbox_uploader.upload('mybinarydata2', 'myotherphoto.jpg')

        dropbox_constructor_mock.assert_called_with('mytoken')
        dropbox_mock.files_upload.assert_has_calls([
            mock.call('mybinarydata', '/my-customer-dir/photo1.png'),
            mock.call('mybinarydata2', '/my-customer-dir/photo2.jpg')
        ])

    @mock.patch('photospicker.uploader.uploaders.dropbox_uploader.Dropbox')
    def test_not_caught_error_on_files_delete(self, dropbox_constructor_mock):
        """
        Test that an ApiError raised by Dropbox client is not caught
        if it's not a path lookup error

        :param MagicMock dropbox_constructor_mock:
                                                mock for dropbox constructor
        """
        dropbox_mock = Mock()
        dropbox_constructor_mock.return_value = dropbox_mock
        dropbox_mock.files_delete_v2.side_effect = ApiError(
            '',
            DeleteError('other'),
            'myerrormessage',
            ''
        )

        with self.assertRaises(ApiError) as cm:
            dropbox_uploader = DropboxUploader(None)
            dropbox_uploader.initialize()

        self.assertEqual("myerrormessage", cm.exception.user_message_text)

    @mock.patch('photospicker.uploader.uploaders.dropbox_uploader.Dropbox')
    def test_caught_error_on_files_delete(self, dropbox_constructor_mock):
        """
        Test that path lookup ApiErrors raised by Dropbox are caught

        :param MagicMock dropbox_constructor_mock:
                                                mock for dropbox constructor
        """
        dropbox_mock = Mock()
        dropbox_constructor_mock.return_value = dropbox_mock
        dropbox_mock.files_delete_v2.side_effect = ApiError(
            '',
            DeleteError('path_lookup', LookupError('not_found')),
            'myerrormessage',
            ''
        )

        dropbox_uploader = DropboxUploader(None)
        dropbox_uploader.initialize()
        dropbox_uploader.upload('mybinarydata', 'myphoto.png')
        dropbox_mock.files_upload.assert_called_with(
            'mybinarydata',
            '/photos-picker/photo0.png'
        )

    def test_constructor_with_wrong_folder_name_should_raise_exception(self):
        """
        Test that the constructor raises an exception if an invalid folder
        name is given
        """
        with self.assertRaises(UploaderException) as cm:
            DropboxUploader(None, 'my_wrong_folder_name!')

        self.assertEqual(
            UploaderException.INVALID_DIR_NAME,
            cm.exception.code
        )
