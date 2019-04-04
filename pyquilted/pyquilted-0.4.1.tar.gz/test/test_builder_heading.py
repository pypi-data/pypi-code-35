import unittest
from pyquilted.builder.heading import HeadingBuilder
from pyquilted.yaml_loader import YamlLoader


class TestBuilderHeading(unittest.TestCase):
    def setUp(self):
        with open('test/validations/heading.yml') as f:
            self.odata = YamlLoader.ordered_load(f)

    def test_heading(self):
        mapper = HeadingBuilder(self.odata['heading'])
        heading = mapper.deserialize()

        self.assertIsNotNone(heading.name)
        self.assertIsNone(heading.primary)
        self.assertIsNone(heading.adjacent)

    def test_location(self):
        mapper = HeadingBuilder(self.odata['heading-location'])
        heading = mapper.deserialize()

        self.assertIsNotNone(heading.name)
        self.assertIsNotNone(heading.primary)
        self.assertIsNone(heading.adjacent)

    def test_heading_simple(self):
        mapper = HeadingBuilder(self.odata['heading-simple'])
        heading = mapper.deserialize()

        self.assertIsNotNone(heading.name)
        self.assertIsNotNone(heading.primary)
        self.assertIsNotNone(heading.adjacent)

    def test_heading_complex(self):
        mapper = HeadingBuilder(self.odata['heading-complex'])
        heading = mapper.deserialize()

        self.assertIsNotNone(heading.name)
        self.assertIsNotNone(heading.primary)
        self.assertIsNotNone(heading.adjacent)
        self.assertIsNotNone(heading.top_side)
        self.assertIsNotNone(heading.bottom_side)


if __name__ == '__main__':
    unittest.main()
