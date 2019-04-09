import unittest
from pyquilted.quilted.section import Section


class MyMockCompoundClass(Section):
    def __init__(self):
        self.one = 1


class Mock(Section):
    def __init__(self):
        self.one = 1


class TestSection(unittest.TestCase):
    def test_kebab(self):
        mock = Mock()
        self.assertEqual(mock._kebab_name(), 'mock')

    def test_kebab_compound(self):
        mock = MyMockCompoundClass()
        self.assertEqual(mock._kebab_name(), 'my-mock-compound-class')

    def test_serialize(self):
        mock = Mock()
        self.assertTrue(isinstance(mock.serialize(), dict))


if __name__ == '__main__':
    unittest.main()
