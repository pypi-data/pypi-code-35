import unittest
from pyquilted.builder.details import HeadingDetailsBuilder
from pyquilted.yaml_loader import YamlLoader


class TestBuilderHeadingDetails(unittest.TestCase):
    def setUp(self):
        with open('test/validations/heading.yml') as f:
            self.odata = YamlLoader.ordered_load(f)

    def test_details_simple(self):
        mapper = HeadingDetailsBuilder(self.odata['heading-simple'])
        heading = mapper.deserialize()

        self.assertIsNotNone(heading.name)
        self.assertIsNone(heading.objective)
        self.assertEqual(len(heading.details), 2)

    def test_details_complex(self):
        mapper = HeadingDetailsBuilder(self.odata['heading-complex'])
        heading = mapper.deserialize()

        self.assertIsNotNone(heading.name)
        self.assertIsNotNone(heading.objective)
        self.assertEqual(len(heading.details), 3)


if __name__ == '__main__':
    unittest.main()
