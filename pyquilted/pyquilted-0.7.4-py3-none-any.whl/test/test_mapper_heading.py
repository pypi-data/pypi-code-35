import unittest
from pyquilted.mapper.heading import HeadingMapper
from pyquilted.yaml_loader import YamlLoader


class TestMapperHeading(unittest.TestCase):
    def setUp(self):
        with open('test/validations/heading.yml') as f:
            self.odata = YamlLoader.ordered_load(f)

    def test_heading(self):
        mapper = HeadingMapper(self.odata['heading'])
        heading = mapper.deserialize()

        self.assertIsNotNone(heading.name)
        self.assertIsNone(heading.primary)
        self.assertIsNone(heading.adjacent)

    def test_location(self):
        mapper = HeadingMapper(self.odata['heading-location'])
        heading = mapper.deserialize()

        self.assertIsNotNone(heading.name)
        self.assertIsNotNone(heading.primary)
        self.assertIsNone(heading.adjacent)

    def test_heading_simple(self):
        mapper = HeadingMapper(self.odata['heading-simple'])
        heading = mapper.deserialize()

        self.assertIsNotNone(heading.name)
        self.assertIsNotNone(heading.primary)
        self.assertIsNotNone(heading.adjacent)

    def test_heading_complex(self):
        pass


if __name__ == '__main__':
    unittest.main()
