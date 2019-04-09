import unittest
from pyquilted.quilted.education import Education


class TestEducation(unittest.TestCase):
    def test_education(self):
        education = Education('school')

        self.assertTrue(hasattr(education, 'value'))
        self.assertEqual(education.label, 'Education')
        self.assertEqual(education.icon, 'fa-graduation-cap')
        self.assertTrue(education.compact)


if __name__ == '__main__':
    unittest.main()
