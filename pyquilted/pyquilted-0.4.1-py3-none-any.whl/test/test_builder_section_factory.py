import unittest
from pyquilted.builder.section_factory import *


class TestSectionBuilderFactory(unittest.TestCase):
    def setUp(self):
        self.builder = SectionBuilderFactory('section_name', {'data': None})

    def test_section_builder_factory(self):

        self.assertIsNotNone(self.builder.key)
        self.assertIsNotNone(self.builder.section_odict)
        self.assertIsNotNone(self.builder.options)

        self.assertIsNone(self.builder.mapper)
        self.assertIsNone(self.builder.section)

        self.assertIsInstance(self.builder.options, SectionOptions)

        self.assertTrue(hasattr(self.builder, 'create_section'))


if __name__ == '__main__':
    unittest.main()
