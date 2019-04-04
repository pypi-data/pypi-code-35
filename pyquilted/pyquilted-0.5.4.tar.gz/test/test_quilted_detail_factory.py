import unittest
from pyquilted.quilted.detail import *
from pyquilted.quilted.detail_factory import DetailFactory


class TestDetailFactory(unittest.TestCase):
    def setUp(self):
        self.factory = DetailFactory()

    def test_detail_factory(self):
        self.assertTrue(hasattr(self.factory, 'create'))

    def test_detail_factory_location(self):
        detail = self.factory.create('location',
                {'location':'Boston', 'via':'car'})
        self.assertIsInstance(detail, Location)

    def test_detail_factory_flair(self):
        detail = self.factory.create('flair', {'data':None})
        self.assertIsInstance(detail, Flair)

    def test_detail_factory_objective(self):
        detail = self.factory.create('objective', {'data':None})
        self.assertIsInstance(detail, Objective)

    def test_detail_factory_title(self):
        detail = self.factory.create('title', {'data':None})
        self.assertIsInstance(detail, Title)


if __name__ == '__main__':
    unittest.main()
