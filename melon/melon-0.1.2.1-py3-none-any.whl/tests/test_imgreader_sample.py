import pathlib
from unittest import TestCase, mock, main

import numpy

from melon import ImageReader


class ImageReaderTestCase(TestCase):
    _tests_dir = "tests/resources/images/sample"

    def test_result_shape(self):
        reader = ImageReader(self._tests_dir)
        x, y = reader.read()
        self.assertEqual((6, 3, 255, 255), x.shape)
        self.assertEqual((6, 5), y.shape)

    def test_result_shape_channels_last(self):
        reader = ImageReader(self._tests_dir, {"data_format": "channels_last"})
        x, y = reader.read()
        self.assertEqual((6, 255, 255, 3), x.shape)
        self.assertEqual((6, 5), y.shape)

    def test_result_shape_label_format(self):
        reader = ImageReader(self._tests_dir, {"label_format": "label"})
        x, y = reader.read()
        self.assertEqual((6, 3, 255, 255), x.shape)
        self.assertEqual((6,), y.shape)

    def test_batch_read_when_no_remainder(self):
        reader = ImageReader(self._tests_dir, {"batch_size": 2})
        self.assertTrue(reader.has_next())
        x, y = reader.read()
        self.assertEqual((2, 3, 255, 255), x.shape)
        self.assertEqual((2, 5), y.shape)

        self.assertTrue(reader.has_next())
        x, y = reader.read()
        self.assertEqual((2, 3, 255, 255), x.shape)
        self.assertEqual((2, 5), y.shape)

        self.assertTrue(reader.has_next())
        x, y = reader.read()
        self.assertEqual((2, 3, 255, 255), x.shape)
        self.assertEqual((2, 5), y.shape)
        self.assertFalse(reader.has_next())

    def test_batch_read_when_remainder(self):
        reader = ImageReader(self._tests_dir, {"batch_size": 5})
        self.assertTrue(reader.has_next())
        x, y = reader.read()
        self.assertEqual((5, 3, 255, 255), x.shape)
        self.assertEqual((5, 5), y.shape)

        self.assertTrue(reader.has_next())
        x, y = reader.read()
        self.assertEqual((1, 3, 255, 255), x.shape)
        self.assertEqual((1, 5), y.shape)

    def test_batch_read_ensure_all_files_were_read(self):
        mock_img_arr = numpy.ndarray((3, 255, 255))
        mock_labels, mock_classes, mock_files = self._mock_meta(25)
        with mock.patch.object(ImageReader, "_read_meta", return_value=(mock_labels, mock_classes, mock_files)):
            with mock.patch.object(ImageReader, '_img_to_arr', return_value=mock_img_arr):
                reader = ImageReader(self._tests_dir, {"batch_size": 3})
                while reader.has_next():
                    x, y = reader.read()
                    for label_vector in y:
                        label = label_vector.tolist().index(1)
                        del mock_labels["img_{}.jpg".format(label)]

                self.assertFalse(reader.has_next())
                self.assertTrue(not mock_labels)

    def test_result_order(self):
        pixels = self._expected_pixels()
        reader = ImageReader(self._tests_dir, {"normalize": False})
        x, y = reader.read()
        for i in range(len(y)):
            label = y[i].tolist().index(1)  # in one-hot-encoding location of 1 should match the label

            first_five_pixels = x[i][0][0][:5]
            expected = pixels[label]
            if label == 1:
                self.assertTrue(numpy.array_equal(expected[0], first_five_pixels) or numpy.array_equiv(expected[1], first_five_pixels))
                continue
            self.assertTrue(numpy.array_equal(expected, first_five_pixels))

        self.assertEqual((6, 3, 255, 255), x.shape)
        self.assertEqual((6, 5), y.shape)

    def test_result_order_when_batch_read(self):
        pixels = self._expected_pixels()
        reader = ImageReader(self._tests_dir, {"normalize": False, "batch_size": 1})
        while reader.has_next():
            x, y = reader.read()
            label = y[0].tolist().index(1)  # in one-hot-encoding location of 1 should match the label
            first_five_pixels = x[0][0][0][:5]
            expected = pixels[label]
            if label == 1:
                self.assertTrue(numpy.array_equal(expected[0], first_five_pixels) or numpy.array_equiv(expected[1], first_five_pixels))
                continue
            self.assertTrue(numpy.array_equal(expected, first_five_pixels))
            self.assertEqual((1, 3, 255, 255), x.shape)
            self.assertEqual((1, 5), y.shape)

    def test_invalid_data_format_should_raise_error(self):
        with self.assertRaises(ValueError) as context:
            reader = ImageReader(self._tests_dir, {"data_format": "bogus_format"})
            reader.read()
            self.assertTrue("Unknown data format" in str(context))

    def test_thread_batch_size_with_remainder(self):
        mock_img_arr = numpy.ndarray((3, 255, 255))
        with mock.patch.object(ImageReader, "_read_meta", return_value=self._mock_meta(18)):
            with mock.patch.object(ImageReader, '_img_to_arr', return_value=mock_img_arr):
                reader = ImageReader(self._tests_dir, {"num_threads": 4})
                x, y = reader.read()
                self.assertEqual((18, 3, 255, 255), x.shape)
                self.assertEqual((18, 18), y.shape)

    @staticmethod
    def _expected_pixels():
        pixels = dict()
        pixels[0] = [0, 0, 0, 0, 0]
        pixels[1] = [[35, 31, 19, 32, 27], [250, 250, 249, 250, 250]]
        pixels[2] = [38, 33, 32, 39, 58]
        pixels[3] = [255, 255, 255, 255, 255]
        pixels[4] = [246, 246, 246, 246, 246]
        return pixels

    @staticmethod
    def _mock_meta(cnt, ext="jpg"):
        mock_files = []
        mock_labels = {}
        mock_classes = set()
        for i in range(0, cnt):
            file_name = "img_{}.{}".format(i, ext)
            mock_files.append(pathlib.Path(file_name))
            mock_labels[file_name] = int(i)
            mock_classes.add(int(i))

        return mock_labels, mock_classes, mock_files


if __name__ == '__main__':
    main()
