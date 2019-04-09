import unittest
from pyquilted.builder.education import EducationBuilder
from pyquilted.yaml_loader import YamlLoader


class TestBuilderEducation(unittest.TestCase):
    def test_mapper_education(self):
        with open('test/validations/education.yml') as f:
            odata = YamlLoader.ordered_load(f)
        mapper = EducationBuilder(odata['education'])
        education = mapper.deserialize()

        valid = {
                "education": {
                    "label": "Education",
                    "value": "The Night's Watch",
                    "icon": "fa-graduation-cap"
                    }
                }
        self.assertEqual(education.serialize(), valid)


if __name__ == '__main__':
    unittest.main()
