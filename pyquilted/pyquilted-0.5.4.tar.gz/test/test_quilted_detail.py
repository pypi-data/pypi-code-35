import unittest
from pyquilted.quilted.detail import *


class MockDetail(Detail):
    def __init__(self):
        pass


class TestDetail(unittest.TestCase):
    def setUp(self):
        self.mock = MockDetail()

    def test_detail(self):
        self.assertTrue(hasattr(self.mock, 'serialize'))

    def test_detail_location(self):
        detail = Location()
        self.assertTrue(hasattr(detail, 'location'))
        self.assertTrue(hasattr(detail, 'via'))

    def test_detail_location_greater(self):
        detail_greater = Location(location='Greater Boston')
        self.assertIsNone(detail_greater.via)

    def test_detail_flair(self):
        detail = Flair()
        self.assertTrue(hasattr(detail, 'flair'))
        self.assertTrue(hasattr(detail, 'icon'))
        self.assertTrue(hasattr(detail, 'link'))

    def test_detail_objective(self):
        detail = Objective()
        self.assertTrue(hasattr(detail, 'objective'))

    def test_detail_title(self):
        detail = Title()
        self.assertTrue(hasattr(detail, 'title'))


if __name__ == '__main__':
    unittest.main()
