import unittest
from pyquilted.quilted.projects import *


class TestProjects(unittest.TestCase):
    def setUp(self):
        self.activity = Activity()
        self.projects = Projects()
        self.projects_x = Projects(blocks=[{}], icon='fa-test')

    def test_activity(self):
        self.assertTrue(hasattr(self.activity, 'name'))
        self.assertTrue(hasattr(self.activity, 'icon'))
        self.assertTrue(hasattr(self.activity, 'link'))
        self.assertTrue(hasattr(self.activity, 'description'))
        self.assertTrue(hasattr(self.activity, 'slugs'))

    def test_projects(self):
        self.assertTrue(hasattr(self.projects, 'label'))
        self.assertTrue(hasattr(self.projects, 'icon'))
        self.assertTrue(hasattr(self.projects, 'blocks'))
        self.assertTrue(hasattr(self.projects, 'add_activity'))
        self.assertTrue(callable(self.projects.add_activity))

        self.assertEqual(self.projects.label, 'Projects')
        self.assertEqual(self.projects.icon, 'fa-code')
        self.assertIsInstance(self.projects.blocks, list)
        self.assertEqual(len(self.projects.blocks), 0)

    def test_projects_x(self):
        self.assertEqual(len(self.projects_x.blocks), 1)
        self.assertEqual(self.projects_x.icon, 'fa-test')

    def test_add_activity(self):
        self.projects.add_activity(self.activity)
        self.assertEqual(len(self.projects.blocks), 1)


if __name__ == '__main__':
    unittest.main()
