import unittest
from pyquilted.quilted.skills import Skills


class TestSkills(unittest.TestCase):
    def setUp(self):
        nskills = ["parkour", "karate", "disco"]
        self.skills = Skills(nskills)
        self.skills_unsorted = Skills(nskills, sort=False)

    def test_skills(self):
        self.assertTrue(hasattr(self.skills, 'sort'))
        self.assertTrue(hasattr(self.skills, 'label'))
        self.assertTrue(hasattr(self.skills, 'icon'))
        self.assertTrue(hasattr(self.skills, 'value'))
        self.assertEqual(self.skills.value, 'disco, karate, parkour')

    def test_skills_unsorted(self):
        self.assertEqual(self.skills_unsorted.value, 'parkour, karate, disco')


if __name__ == '__main__':
    unittest.main()
