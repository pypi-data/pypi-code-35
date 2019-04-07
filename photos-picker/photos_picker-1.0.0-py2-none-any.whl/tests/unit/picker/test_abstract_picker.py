from photospicker.exception.picker_exception import PickerException
from photospicker.picker.abstract_picker import AbstractPicker
from unittest import TestCase
from mock import MagicMock  # noqa
from mock import Mock
import unittest_dataprovider
import mock
from tests.unit.picker.picker_photo_stub import PickerPhotoStub


class DummyPicker(AbstractPicker):
    """Dummy class for testing AbstractPicker"""

    def _scan(self):
        """Dummy abstract method"""
        pass

    @property
    def files_to_scan(self):
        """
        Getter for _files_to_scan

        :return: list
        """
        return self._files_to_scan

    def photos_count(self):
        """
        Getter for _photos_count

        :return: int
        """
        return self._photos_count


class TestAbstractPicker(TestCase):
    """Unit tests for AbstractPicker"""

    def test_wrong_patterns_format(self):
        """Test that an exception is launched """
        with self.assertRaises(TypeError) as cm:
            DummyPicker('', 20, patterns='test')

        self.assertEqual(
            "patterns argument must be a list",
            str(cm.exception)
        )

    @staticmethod
    def provider_analyse():
        """Data provider for test_initialize"""
        return (
            (None, ['myphoto1.jpg', 'myphoto2.JPEG', 'myphoto3.png']),
            (['*.jpg', '*.jpeg'], ['myphoto1.jpg', 'myphoto2.JPEG']),
        )

    @unittest_dataprovider.data_provider(provider_analyse)
    @mock.patch('os.walk')
    def test_initialize(self, patterns, expected_files_to_scan, walk_mock):
        """
        Test initialize method

        :param list|None patterns: patterns passed to the constructor
        :param list expected_files_to_scan: list that should be in
                                            the _files_to_scan property
        :param MagicMock walk_mock: mock for walk function
        """

        walk_mock.return_value = [['', [], [
            'myphoto1.jpg',
            'myphoto2.JPEG',
            'myphoto3.png'
        ]]]

        sut = DummyPicker('mypath', 20, patterns=patterns)
        sut.initialize()

        walk_mock.assert_called_with('mypath')
        self.assertEqual(
            [PickerPhotoStub(filepath) for filepath in expected_files_to_scan],
            sut.files_to_scan
        )

    @staticmethod
    def provider_initialize_multiple_and_excluded_paths():
        """Data provider for test_initialize_multiple_and_excluded_paths"""
        return (
            ([], [
                '/mypath1/folder1/myphoto1.jpg',
                '/mypath1/folder1/myphoto2.JPEG',
                '/home/user/mypath2/myphoto3.png',
                '/home/user/mypath2/folder1/myphoto4.png'
            ]),
            (['/folder1/'], [
                '/home/user/mypath2/myphoto3.png'
            ]),
            (['/mypath1'], [
                '/home/user/mypath2/myphoto3.png',
                '/home/user/mypath2/folder1/myphoto4.png'
            ]),
            (['~/mypath2'], [
                '/mypath1/folder1/myphoto1.jpg',
                '/mypath1/folder1/myphoto2.JPEG',
            ]),
            (['~user/mypath2'], [
                '/mypath1/folder1/myphoto1.jpg',
                '/mypath1/folder1/myphoto2.JPEG'
            ]),
            (['/home/user/mypath2/folder1'], [
                '/mypath1/folder1/myphoto1.jpg',
                '/mypath1/folder1/myphoto2.JPEG',
                '/home/user/mypath2/myphoto3.png'
            ])
        )

    @unittest_dataprovider.data_provider(
        provider_initialize_multiple_and_excluded_paths
    )
    @mock.patch('os.path.expanduser')
    @mock.patch('os.walk')
    def test_initialize_multiple_and_excluded_paths(
            self,
            excluded_paths,
            expected_files_to_scan,
            walk_mock,
            expanduser_mock
    ):
        """
        Test initialize method with multiple and excluded paths

        :param list excluded_paths: excluded paths
        :param list expected_files_to_scan: expected files to scan
        :param MagicMock walk_mock: mock for walk function
        :param MagicMock expanduser_mock: mock for expanduser function
        """
        expanduser_mock.side_effect = self.expanduser_side_effect

        walk_mock.side_effect = [
            [
                ['/mypath1', [], []],
                ['/mypath1/folder1', [], ['myphoto1.jpg', 'myphoto2.JPEG']]
            ],
            [
                ['/home/user/mypath2', [], ['myphoto3.png']],
                ['/home/user/mypath2/folder1', [], ['myphoto4.png']]
            ]
        ]

        sut = DummyPicker(
            ['/mypath1', '~/mypath2'],
            20,
            0,
            None,
            excluded_paths
        )
        sut.initialize()

        walk_mock.assert_has_calls([
            mock.call('/mypath1'),
            mock.call('/home/user/mypath2')
        ])

        self.assertEqual(
            [PickerPhotoStub(filepath) for filepath in expected_files_to_scan],
            sut.files_to_scan
        )

    @staticmethod
    def expanduser_side_effect(path):
        """
        Side effect method for expanduser mock

        :param str path: path to expand

        :return: str
        """
        return path.replace('~user', '/home/user').replace('~', '/home/user')

    @mock.patch('os.walk')
    def test_initialize_with_no_photo_found(self, walk_mock):
        """
        Test than an exception is raised when no photo is found in scan path(s)

        :param MagicMock walk_mock        : mock for walk function
        """
        walk_mock.return_value = []

        sut = DummyPicker('/mypath', 20)

        with self.assertRaises(PickerException) as cm:
            sut.initialize()

        self.assertEqual(PickerException.EMPTY_SCAN, cm.exception.code)

    @mock.patch('os.walk')
    def test_photos_count_greater_than_total_photos(self, walk_mock):
        """
        Test that _photos_count is updated if greater than total photos count

        :param MagicMock walk_mock: mock for walk function
        """
        walk_mock.side_effect = [
            [
                ['/mypath', [], [
                    'myphoto1.jpg', 'myphoto2.jpg', 'myphoto3.jpg',
                    'myphoto4.jpg', 'myphoto5.jpg', 'myphoto6.jpg',
                    'myphoto7.jpg', 'myphoto8.jpg', 'myphoto9.jpg'
                ]]
            ]
        ]

        sut = DummyPicker('/mypath', 12)
        sut.initialize()
        self.assertEqual(9, sut.photos_count())

    @staticmethod
    def provider_scan():
        """
        Data provider for test_scan

        :return: tuple
        """
        return (
            (0, ['myfile3.jpg', 'myfile1.jpg', 'myfile4.jpg', 'myfile2.jpg']),
            (-1, ['myfile2.jpg', 'myfile3.jpg', 'myfile4.jpg', 'myfile1.jpg']),
            (1, ['myfile1.jpg', 'myfile4.jpg', 'myfile3.jpg', 'myfile2.jpg'])
        )

    @unittest_dataprovider.data_provider(provider_scan)
    @mock.patch('random.shuffle')
    def test_scan(self, order_parameter, expected_picked, shuffle_mock):
        """
        Test scan method

        :param MagicMock shuffle_mock: mock for shuffle method
        :param int order_parameter: parameter given to constructor for ordering
        :param list expected_picked: expected sorted list
        """
        internal_scan_mock = Mock()
        internal_scan_mock.return_value = [
            PickerPhotoStub('myfile1.jpg', '2018-04-07 23:32:21'),
            PickerPhotoStub('myfile2.jpg', '2018-05-05 18:32:21'),
            PickerPhotoStub('myfile3.jpg', '2018-05-05 12:32:21'),
            PickerPhotoStub('myfile4.jpg', '2018-05-03 15:32:21'),
        ]

        shuffle_mock.side_effect = self._random_shuffle_side_effect

        sut = DummyPicker('', 0, order_parameter)
        sut._scan = internal_scan_mock
        sut.scan()

        self.assertEqual(
            expected_picked,
            sut.picked_file_paths
        )

    def _random_shuffle_side_effect(self, photos):
        """
        Side effect for random shuffle

        :param list photos: list of PickerPhotoStub objects
        """
        self.assertEqual([
            PickerPhotoStub('myfile1.jpg', '2018-04-07 23:32:21'),
            PickerPhotoStub('myfile2.jpg', '2018-05-05 18:32:21'),
            PickerPhotoStub('myfile3.jpg', '2018-05-05 12:32:21'),
            PickerPhotoStub('myfile4.jpg', '2018-05-03 15:32:21'),
        ], photos)

        photo1 = photos[0]
        photo2 = photos[1]
        photo3 = photos[2]
        photo4 = photos[3]
        del photos[:]
        photos.append(photo3)
        photos.append(photo1)
        photos.append(photo4)
        photos.append(photo2)
