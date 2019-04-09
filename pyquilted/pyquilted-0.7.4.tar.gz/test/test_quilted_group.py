import unittest
from pyquilted.quilted.group import Group


class TestGroup(unittest.TestCase):
    def setUp(self):
        self.group = Group()

    def test_group(self):
        self.assertTrue(hasattr(self.group, 'blocks'))
        self.assertTrue(hasattr(self.group, 'add_section'))
        self.assertTrue(hasattr(self.group, 'get_sections'))

        self.assertIsInstance(self.group.blocks, list)
        self.assertTrue(callable(self.group.add_section))
        self.assertTrue(callable(self.group.get_sections))

    def test_group_add_section(self):
        self.group.add_section({'one': 1})
        self.assertEqual(len(self.group.blocks), 1)

    def test_group_get_section_single(self):
        self.group.add_section({'one': 1})
        sblocks = self.group.get_sections()

        self.assertTrue('one' in sblocks)

    def test_group_get_section_more(self):
        self.group.add_section({'one': 1})
        self.group.add_section({'two': 2})
        mblocks = self.group.get_sections()

        self.assertTrue('group' in mblocks)


if __name__ == '__main__':
    unittest.main()
