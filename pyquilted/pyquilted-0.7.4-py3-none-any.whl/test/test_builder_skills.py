import unittest
from pyquilted.builder.skills import SkillsBuilder
from pyquilted.quilted.skills import Skills
from pyquilted.quilted.skills_table import SkillsTable


class TestBuilderSkills(unittest.TestCase):
    def setUp(self):
        skills = ["karate", "joust", "parkour", "spooning", "youtubing", "dev"]
        self.builder = SkillsBuilder(skills)
        self.builder_table = SkillsBuilder(skills, table=True)

    def test_builder_skills(self):
        self.assertTrue(hasattr(self.builder, 'odict'))
        self.assertTrue(hasattr(self.builder, 'table'))
        self.assertTrue(hasattr(self.builder, 'sorting'))

        self.assertTrue(self.builder.sorting)
        self.assertFalse(self.builder.table)
        self.assertIsInstance(self.builder.odict, list)

        self.assertTrue(self.builder_table.table)

    def test_builder_deserialize(self):
        skills_default = self.builder.deserialize()
        skills_x = self.builder_table.deserialize()
        self.assertIsInstance(skills_default, Skills)
        self.assertIsInstance(skills_x, SkillsTable)


if __name__ == '__main__':
    unittest.main()
