import unittest
from pyquilted.builder.section_factory import SectionOptions


class TestSectionOptions(unittest.TestCase):
    def setUp(self):
        self.options_default = SectionOptions()
        self.options = SectionOptions(heading='compact')

    def test_section_options_default(self):
        self.assertIsNotNone(self.options_default.heading)
        self.assertEqual(self.options_default.heading, 'auto')

    def test_section_options(self):
        self.assertIsNotNone(self.options.heading)
        self.assertEqual(self.options.heading, 'compact')


if __name__ == '__main__':
    unittest.main()
