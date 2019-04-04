import inspect
import unittest
from pyquilted.app_factory import *
from pyquilted.builder.section_factory import SectionOptions
from pyquilted.quilted.style_options import StyleOptions


class MockArgs():
    def __init__(self):
        self.one = 1


class TestAppFactory(unittest.TestCase):
    def test_app_factory(self):
        factory = AppFactory(MockArgs())

        self.assertTrue(hasattr(factory, 'args'))
        self.assertTrue(hasattr(factory, 'options'))
        self.assertTrue(hasattr(factory, 'section_options'))
        self.assertTrue(hasattr(factory, 'style_options'))

        self.assertTrue(isinstance(factory.args, dict))
        self.assertTrue(isinstance(factory.style_options, dict))
        self.assertTrue(isinstance(factory.options, AppOptions))
        self.assertTrue(isinstance(factory.section_options, SectionOptions))

        self.assertTrue(inspect.ismethod(factory.create))


if __name__ == '__main__':
    unittest.main()
