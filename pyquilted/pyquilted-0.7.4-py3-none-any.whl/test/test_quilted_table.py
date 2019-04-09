import unittest
from pyquilted.quilted.table import *


class TestTable(unittest.TestCase):
    def setUp(self):
        self.columns = Columns(size=3, default="empty")
        self.columns_small = Columns()
        self.values = [0, 1, 2, 3, 4]
        self.table = Table(cols=3, default=-1)

    def test_column(self):
        self.assertTrue(hasattr(self.columns, 'size'))
        self.assertTrue(hasattr(self.columns, 'items'))
        self.assertTrue(hasattr(self.columns, 'default'))
        self.assertTrue(hasattr(self.columns, 'add_item'))
        self.assertTrue(hasattr(self.columns, 'to_dict'))

        self.assertIsInstance(self.columns.items, list)
        self.assertTrue(callable(self.columns.add_item))
        self.assertTrue(callable(self.columns.to_dict))

    def test_column_add_item(self):
        self.columns_small.add_item("one")
        self.assertEqual(len(self.columns_small.items), 1)

    def test_column_add_item_limit(self):
        self.columns_small.add_item("two")
        self.assertEqual(len(self.columns_small.items), 1)

    def test_column_to_dict(self):
        self.columns.add_item("one")
        valid_one = {"cols": ["one", "empty", "empty"]}
        self.assertEqual(self.columns.to_dict(), valid_one)

        self.columns.add_item("two")
        valid_two = {"cols": ["one", "two", "empty"]}
        self.assertEqual(self.columns.to_dict(), valid_two)

    def test_table(self):
        self.assertTrue(hasattr(self.table, 'col_size'))
        self.assertTrue(hasattr(self.table, 'default'))
        self.assertTrue(hasattr(self.table, 'rows'))
        self.assertTrue(hasattr(self.table, 'build'))

        self.assertIsInstance(self.table.rows, list)
        self.assertTrue(callable(self.table.build))

    def test_table_build(self):
        rows = self.table.build(self.values)
        self.assertEqual(len(rows), 2)
        valid = [{'cols': [0, 1, 2]}, {'cols': [3, 4, -1]}]
        self.assertEqual(rows, valid)


if __name__ == '__main__':
    unittest.main()
