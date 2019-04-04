import unittest
from pyquilted.builder.skills import SkillsBuilder
from pyquilted.yaml_loader import YamlLoader


class TestBuilderSkills(unittest.TestCase):
    def test_mapper_skills(self):
        with open('test/validations/skills.yml') as f:
            data = YamlLoader.ordered_load(f)
        mapper = SkillsBuilder(data['skills'])
        skills = mapper.deserialize()

        valid = {
                "skills": {
                    "label": "Skills",
                    "value": "Bravery, Leadership, Swordsmanship, "
                             "Brooding, Knowing-nothing, HTML",
                    "icon": "fa-wrench"
                    }
                }
        self.assertEqual(skills.serialize(), valid)


if __name__ == '__main__':
    unittest.main()
