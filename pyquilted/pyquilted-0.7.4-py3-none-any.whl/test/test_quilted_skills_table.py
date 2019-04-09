import unittest
from pyquilted.quilted.skills_table import SkillsTable


class TestSkillsTable(unittest.TestCase):
    def setUp(self):
        skills = ["karate", "disco", "influencer", "parkour", "joust"]
        self.skills_table = SkillsTable(skills, cols=3, default="")

    def test_skills_table(self):
        self.assertTrue(hasattr(self.skills_table, 'sort'))
        self.assertTrue(hasattr(self.skills_table, 'label'))
        self.assertTrue(hasattr(self.skills_table, 'icon'))
        self.assertTrue(hasattr(self.skills_table, 'compact'))
        self.assertTrue(hasattr(self.skills_table, 'rows'))

        self.assertFalse(self.skills_table.compact)
        self.assertIsInstance(self.skills_table.rows, list)


if __name__ == '__main__':
    unittest.main()
