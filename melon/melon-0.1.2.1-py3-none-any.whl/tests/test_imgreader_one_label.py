from unittest import TestCase, main

import numpy

from melon import ImageReader


class ImageReaderTestCase(TestCase):
    _tests_dir = "tests/resources/images/one_label"

    def test_result_shape(self):
        reader = ImageReader(self._tests_dir)
        x, y = reader.read()
        self.assertEqual((2, 3, 255, 255), x.shape)
        self.assertEqual((2, 3), y.shape)

    def test_result_shape_label_format(self):
        reader = ImageReader(self._tests_dir, {"label_format": "label"})
        x, y = reader.read()
        self.assertEqual((2, 3, 255, 255), x.shape)
        self.assertEqual((2,), y.shape)

    def test_result_order(self):
        expected = [[35, 31, 19, 32, 27], [250, 250, 249, 250, 250]]
        reader = ImageReader(self._tests_dir, {"normalize": False})
        x, y = reader.read()
        for i in range(len(y)):
            self.assertEqual(2, y[i].tolist().index(1))
            first_five_pixels = x[i][0][0][:5]
            self.assertTrue(numpy.array_equal(expected[0], first_five_pixels) or numpy.array_equiv(expected[1], first_five_pixels))

        self.assertEqual((2, 3, 255, 255), x.shape)
        self.assertEqual((2, 3), y.shape)


if __name__ == '__main__':
    main()
