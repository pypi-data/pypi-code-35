from unittest import TestCase, main

from melon import ImageReader


class ImageReaderTestCase(TestCase):
    _tests_dir = "tests/resources/images/unsupported_files"

    def test_result_shape(self):
        reader = ImageReader(self._tests_dir)
        x, y = reader.read()
        self.assertEqual(0, x.size)
        self.assertEqual(0, y.size)


if __name__ == '__main__':
    main()
