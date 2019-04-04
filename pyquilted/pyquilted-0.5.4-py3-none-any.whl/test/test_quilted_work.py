import unittest
from pyquilted.quilted.work import *


class TestWork(unittest.TestCase):
    def setUp(self):
        self.slugs = Slugs()
        self.job = Job()
        self.work = Work()
        self.history = History()
        self.history_x = History(previously=['company'])


    def test_slugs(self):
        self.assertTrue(hasattr(self.slugs, 'blocks'))

    def test_job(self):
        self.assertTrue(hasattr(self.job, 'dates'))
        self.assertTrue(hasattr(self.job, 'location'))
        self.assertTrue(hasattr(self.job, 'company'))
        self.assertTrue(hasattr(self.job, 'title'))
        self.assertTrue(hasattr(self.job, 'history'))
        self.assertTrue(hasattr(self.job, 'slugs'))

    def test_work(self):
        self.assertTrue(hasattr(self.work, 'label'))
        self.assertTrue(hasattr(self.work, 'icon'))
        self.assertTrue(hasattr(self.work, 'blocks'))
        self.assertTrue(hasattr(self.work, 'add_job'))
        self.assertTrue(hasattr(self.work, 'add_slugs'))

        self.assertTrue(callable(self.work.add_job))
        self.assertTrue(callable(self.work.add_slugs))

    def test_history(self):
        self.assertTrue(hasattr(self.history, 'previously'))
        self.assertTrue(hasattr(self.history, 'to_dict'))
        self.assertTrue(callable(self.history.to_dict))

    def test_history_to_dict(self):
        self.assertIsNone(self.history.to_dict())
        self.assertIsNotNone(self.history_x.to_dict())


if __name__ == '__main__':
    unittest.main()
