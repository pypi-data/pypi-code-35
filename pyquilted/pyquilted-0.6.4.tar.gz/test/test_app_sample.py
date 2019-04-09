import inspect
import unittest
from pyquilted.sample_app import SampleApp


class TestAppSample(unittest.TestCase):
    def test_app_sample(self):
        app = SampleApp("/src", "dst.yml")

        self.assertTrue(hasattr(app, 'src'))
        self.assertTrue(hasattr(app, 'dst'))
        self.assertTrue(inspect.ismethod(app.run))


if __name__ == '__main__':
    unittest.main()
