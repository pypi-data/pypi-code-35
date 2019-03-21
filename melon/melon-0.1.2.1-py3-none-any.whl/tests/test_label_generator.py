from unittest import TestCase, main

from melon import LabelGenerator
from pathlib import Path


class LabelGeneratorTestCase(TestCase):
    _test_dir = "tests/resources/images/label_generator"
    _labels_file = Path(_test_dir) / LabelGenerator._default_labels_file_name

    def setUp(self):
        self._label_generator = LabelGenerator()

    def test_label_generator_result(self):
        if self._labels_file.exists():
            self._labels_file.unlink()
        expected = set()
        expected.add("img275.jpg")
        expected.add("img928.jpg")
        self._label_generator.generate_labels(self._test_dir)
        cnt = 0
        read_files = False
        with open(str(self._labels_file)) as infile:
            for line in infile:
                line = line.strip()
                if not line: continue
                if line == "#map":
                    read_files = True
                    continue
                if read_files:
                    parts = line.split(":")
                    self.assertTrue(parts[0].strip() in expected)
                    cnt += 1

        self.assertEqual(len(expected), cnt)

    def test_label_generator_raises_error_if_exists(self):
        if not self._labels_file.exists():
            self._labels_file.touch()

        with self.assertRaises(ValueError) as test_context:
            self._label_generator.generate_labels(self._test_dir)
            self.assertTrue("Labels file already exists." in str(test_context.exception))


if __name__ == '__main__':
    main()
