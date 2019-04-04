import unittest
from pyquilted.quilted.iconify import Iconify


class Stub(Iconify):
    def __init__(self):
        pass


class TestIconify(unittest.TestCase):
    def setUp(self):
        self.stub = Stub()

    def test_iconify_mixin(self):
        self.assertTrue(hasattr(self.stub, 'iconify'))
        self.assertTrue(callable(self.stub.iconify))

    def test_iconify(self):
        icon_none = self.stub.iconify(value=None)
        icon_default = self.stub.iconify(value=None, default='fa-icon')
        icon = self.stub.iconify(value='icon')

        self.assertIsNone(icon_none)
        self.assertEqual(icon_default, 'fa-icon')
        self.assertEqual(icon, 'fa-icon')


if __name__ == '__main__':
    unittest.main()
