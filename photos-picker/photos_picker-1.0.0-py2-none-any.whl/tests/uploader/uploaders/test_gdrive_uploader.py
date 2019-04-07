from unittest import TestCase
from mock import Mock, MagicMock
from photospicker.exception.uploader_exception import UploaderException
from photospicker.uploader.uploaders.gdrive_uploader import GDriveUploader
import mock


class TestGDriveUploader(TestCase):
    """Test class for GDriveUploader"""

    def setUp(self):
        self._gauth = Mock()

    @mock.patch('photospicker.uploader.uploaders.gdrive_uploader.GoogleDrive')
    def test_initialize_should_throw_exception_if_many_folders(
            self,
            gdrive_constructor_mock
    ):
        """
        Test that an exception is thrown if there is many directories
        with the name of the photos picker directory

        :param MagicMock gdrive_constructor_mock:
                                                    mock for gdrive constructor
        """
        self._initialize_gdrive_mock(
            gdrive_constructor_mock,
            [[Mock(), Mock()]]
        )

        with self.assertRaises(UploaderException) as cm:
            sut = GDriveUploader(self._gauth, 'my-customer-dir')
            sut.initialize()

        self._initialize_common_assertions(gdrive_constructor_mock)

        self.assertEqual(UploaderException.MANY_DIRS, cm.exception.code)

    @mock.patch('photospicker.uploader.uploaders.gdrive_uploader.GoogleDrive')
    def test_initialize_with_no_existing_folder_should_create_folder(
            self,
            gdrive_constructor_mock
    ):
        """
        Test that if no folder exists with the name of the photos picker
        directory, it is created

        :param MagicMock gdrive_constructor_mock:
                                                    mock for gdrive constructor
        """
        gdrive_mock = self._initialize_gdrive_mock(
            gdrive_constructor_mock,
            [[]]
        )

        created_folder_mock = Mock()
        gdrive_mock.CreateFile.return_value = created_folder_mock

        sut = GDriveUploader(self._gauth, 'my-customer-dir')
        sut.initialize()

        gdrive_mock.CreateFile.assert_called_once_with({
            'mimeType': 'application/vnd.google-apps.folder',
            'title': 'my-customer-dir'
        })
        created_folder_mock.Upload.assert_called_once()

        self._initialize_common_assertions(gdrive_constructor_mock)

    @mock.patch('photospicker.uploader.uploaders.gdrive_uploader.GoogleDrive')
    def test_initialize_with_existing_folder_should_empty_it(
            self,
            gdrive_constructor_mock
    ):
        """
        Test that if a folder already exists with the name of the photos picker
        directory, it is emptied

        :param MagicMock gdrive_constructor_mock:
                                                    mock for gdrive constructor
        """
        folder_mock = MagicMock()
        folder_mock.__getitem__.return_value = 7
        file1 = Mock()
        file2 = Mock()
        self._initialize_gdrive_mock(
            gdrive_constructor_mock,
            [[folder_mock], [file1, file2]]
        )

        sut = GDriveUploader(self._gauth, 'my-customer-dir')
        sut.initialize()

        folder_mock.__getitem__.assert_called_once_with('id')

        self._initialize_common_assertions(
            gdrive_constructor_mock,
            [mock.call({'q': "'7' in parents and trashed=false"})]
        )

        file1.Delete.assert_called_once()
        file2.Delete.assert_called_once()

    @staticmethod
    def _initialize_gdrive_mock(gdrive_constructor_mock, return_values):
        """
        Create a mock for gdrive GetList method

        :param MagicMock gdrive_constructor_mock:
                                                    mock for gdrive constructor
        :param list return_values: values successively
                                                    returned by GetList method

        :return: Mock
        """
        gdrive_mock = Mock()
        gdrive_constructor_mock.return_value = gdrive_mock

        side_effect = []
        for return_value in return_values:
            gdrive_list_mock = Mock()
            gdrive_list_mock.GetList.return_value = return_value
            side_effect.append(gdrive_list_mock)

        gdrive_mock.ListFile.side_effect = side_effect

        return gdrive_mock

    def _initialize_common_assertions(
            self,
            gdrive_constructor_mock,
            list_files_additonal_calls=[]
    ):
        """
        Make common assertions for initialize tests

        :param MagicMock gdrive_constructor_mock:
                                                    mock for gdrive constructor
        :param list list_files_additonal_calls:
                                additional expected calls for ListFile method
        """
        gdrive_constructor_mock.assert_called_once_with(self._gauth)

        calls = [
            mock.call({
                'q': "mimeType = 'application/vnd.google-apps.folder' "
                     "and title = 'my-customer-dir' and trashed=false"
            })
        ]

        calls += list_files_additonal_calls

        gdrive_constructor_mock.return_value.ListFile.assert_has_calls(calls)

    @mock.patch('photospicker.uploader.uploaders.gdrive_uploader.GoogleDrive')
    def test_upload(self, gdrive_constructor_mock):
        """
        Test upload method

        :param MagicMock gdrive_constructor_mock:
                                                    mock for gdrive constructor
        """
        folder_mock = MagicMock()
        folder_mock.__getitem__.return_value = 12
        gdrive_mock = self._initialize_gdrive_mock(
            gdrive_constructor_mock,
            [[folder_mock], []]
        )

        created_file_mock = Mock()
        gdrive_mock.CreateFile.return_value = created_file_mock

        sut = GDriveUploader(self._gauth)
        sut.initialize()
        sut.upload('mybinarydata', 'IMG5423.JPG')

        folder_mock.__getitem__.assert_called_with('id')

        gdrive_mock.CreateFile.assert_called_once_with({
            'parents': [{'kind': 'drive#fileLink', 'id': 12}],
            'title': 'photo0.jpg'
        })

        self.assertEqual('mybinarydata', created_file_mock.content.getvalue())
        created_file_mock.Upload.assert_called_once()

    def test_constructor_with_wrong_folder_name_should_raise_exception(self):
        """
        Test that the constructor raises an exception if an invalid folder
        name is given
        """
        with self.assertRaises(UploaderException) as cm:
            GDriveUploader(None, 'my_wrong_folder_name!')

        self.assertEqual(
            UploaderException.INVALID_DIR_NAME,
            cm.exception.code
        )
