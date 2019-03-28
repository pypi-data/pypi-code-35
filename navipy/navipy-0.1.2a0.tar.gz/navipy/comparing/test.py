import unittest
import numpy as np
from navipy import database
from navipy import comparing
from navipy.scene import is_numeric_array
import pkg_resources


class TestCase(unittest.TestCase):
    def setUp(self):
        """ loads the database """
        self.mydb_filename = pkg_resources.resource_filename(
            'navipy', 'resources/database.db')
        self.mydb = database.DataBase(self.mydb_filename)

    def test_imagediff_curr(self):
        """
        this test checks the function imdiff works
        correctly.
        it checks if correct errors are raised for:
        - frame containing nans
        - frame has wrong dimension

        and checks if the returned frame is correct:
        - has correct shape
        - does not contain nans
        - contains only numeric values
        """
        curr = self.mydb.scene(rowid=1)
        mem = self.mydb.scene(rowid=2)
        curr2 = curr.copy()
        curr2[3, 5, 2, 0] = np.nan
        curr3 = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        curr3 = [curr3, curr3, curr3]
        curr3 = np.array(curr3)
        curr4 = np.zeros((3, 4, 5, 0))

        # put useless stuff here
        with self.assertRaises(ValueError):
            comparing.imagediff(curr2, mem)
        with self.assertRaises(Exception):
            comparing.imagediff(curr3, mem)
        with self.assertRaises(Exception):
            comparing.imagediff(curr4, mem)

        # should be working -> check if result is correct
        for s in [curr]:
            diff = comparing.imagediff(s, mem)
            # self.assertTrue(diff.shape[1] == 1)
            self.assertTrue(diff.shape[0] > 0)
            self.assertFalse(np.any(np.isnan(diff)))
            self.assertTrue(is_numeric_array(diff))

    def test_imagediff_memory(self):
        """
        this test checks the function imagediff works
        correctly for the parameter memory.
        it checks if correct errors are raised for:
        - memory containing nans
        - memory has wrong dimension

        and checks if the returned frame is correct:
        - has correct shape
        - does not contain nans
        - contains only numeric values
        """
        curr = self.mydb.scene(rowid=1)
        mem = self.mydb.scene(rowid=2)
        mem2 = curr.copy()
        mem2[3, 5, 2] = np.nan
        mem3 = [[1, 2], [1, 2], [1, 2]]
        mem3 = [mem3, mem3, mem3]
        mem3 = np.array(mem3)
        mem4 = np.zeros((3, 4, 5))

        with self.assertRaises(ValueError):
            comparing.imagediff(curr, mem2)
        with self.assertRaises(Exception):
            comparing.imagediff(curr, mem3)
        with self.assertRaises(Exception):
            comparing.imagediff(curr, mem4)

        # should be working -> check if result is correct
        for s in [mem]:
            diff = comparing.imagediff(curr, s)
            self.assertFalse(diff.shape[0] <= 0)
            # self.assertTrue(diff.shape[1] == 1)
            self.assertFalse(np.any(np.isnan(diff)))
            self.assertTrue(is_numeric_array(diff))

    def test_rot_imagediff_curr(self):
        """
        this test checks the function imagediff works
        correctly for the parameter current.
        it checks if correct errors are raised for:
        - memory containing nans
        - memory has wrong dimension

        and checks if the returned frame is correct:
        - has correct shape
        - does not contain nans
        - contains only numeric values
        """
        curr = self.mydb.scene(rowid=1)
        mem = self.mydb.scene(rowid=2)
        curr2 = curr.copy()
        curr2[3, 5, 2] = np.nan
        curr3 = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        curr3 = [curr3, curr3, curr3]
        curr3 = np.array(curr3)
        curr4 = np.zeros((3, 4, 5))

        with self.assertRaises(ValueError):
            comparing.rot_imagediff(curr2, mem)
        with self.assertRaises(Exception):
            comparing.rot_imagediff(curr3, mem)
        with self.assertRaises(Exception):
            comparing.rot_imagediff(curr4, mem)

        # should be working -> check if result is correct
        for s in [curr]:
            diff = comparing.rot_imagediff(s, mem)
            self.assertFalse(diff.shape[0] <= 0)
            self.assertTrue(diff.shape[1] == 4)
            self.assertFalse(np.any(np.isnan(diff)))
            self.assertTrue(is_numeric_array(diff))

    def test_rotimagediff_memory(self):
        """
        this test checks the function rot_imagediff works
        correctly for the parameter memory.
        it checks if correct errors are raised for:
        - memory containing nans
        - memory has wrong dimension

        and checks if the returned frame is correct:
        - has correct shape
        - does not contain nans
        - contains only numeric values
        """
        curr = self.mydb.scene(rowid=1)
        mem = self.mydb.scene(rowid=2)
        mem2 = curr.copy()
        mem2[3, 5, 2] = np.nan
        mem3 = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        mem3 = [mem3, mem3, mem3]
        mem3 = np.array(mem3)
        mem4 = np.zeros((3, 4, 5))

        with self.assertRaises(ValueError):
            comparing.rot_imagediff(curr, mem2)
        with self.assertRaises(Exception):
            comparing.rot_imagediff(curr, mem3)
        with self.assertRaises(Exception):
            comparing.rot_imagediff(curr, mem4)

        # should be working -> check if result is correct
        for s in [mem]:
            diff = comparing.rot_imagediff(curr, s)
            self.assertFalse(diff.shape[0] <= 0)
            self.assertTrue(diff.shape[1] == 4)
            self.assertFalse(np.any(np.isnan(diff)))
            self.assertTrue(is_numeric_array(diff))

    def test_simple_imagediff_curr(self):
        """
        this test checks the function simple_imagediff works
        correctly for the parameter current.
        it checks if correct errors are raised for:
        - memory containing nans
        - memory has wrong dimension

        and checks if the returned frame is correct:
        - has correct shape
        - does not contain nans
        - contains only numeric values
        """
        curr = self.mydb.scene(rowid=1)
        mem = self.mydb.scene(rowid=2)
        curr2 = curr.copy()
        curr2[3, 5, 2] = np.nan
        curr3 = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        curr3 = [curr3, curr3, curr3]
        curr3 = np.array(curr3)
        curr4 = np.zeros((3, 4, 5))

        with self.assertRaises(ValueError):
            comparing.simple_imagediff(curr2, mem)
        with self.assertRaises(Exception):
            comparing.simple_imagediff(curr3, mem)
        with self.assertRaises(Exception):
            comparing.simple_imagediff(curr4, mem)

        # should be working -> check if result is correct
        for s in [curr]:
            diff = comparing.simple_imagediff(s, mem)
            self.assertFalse(diff.shape[0] <= 0)
            self.assertTrue(diff.shape[1] > 0)
            self.assertFalse(np.any(np.isnan(diff)))
            self.assertTrue(is_numeric_array(diff))
            self.assertTrue(diff.shape[2] == 4)
            # self.assertTrue(diff.shape[3] == 1)

    def test_simple_imagediff_mem(self):
        """
        this test checks the function imagediff works
        correctly for the parameter memory.
        it checks if correct errors are raised for:
        - memory containing nans
        - memory has wrong dimension

        and checks if the returned frame is correct:
        - has correct shape
        - does not contain nans
        - contains only numeric values
        """
        curr = self.mydb.scene(rowid=1)
        mem = self.mydb.scene(rowid=2)
        mem2 = curr.copy()
        mem2[3, 5, 2] = np.nan
        mem3 = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        mem3 = [mem3, mem3, mem3]
        mem3 = np.array(mem3)
        mem4 = np.zeros((3, 4, 5))

        with self.assertRaises(ValueError):
            comparing.simple_imagediff(curr, mem2)
        with self.assertRaises(Exception):
            comparing.simple_imagediff(curr, mem3)
        with self.assertRaises(Exception):
            comparing.simple_imagediff(curr, mem4)

        # should be working -> check if result is correct
        for s in [mem]:
            diff = comparing.simple_imagediff(curr, s)
            self.assertFalse(diff.shape[0] <= 0)
            self.assertTrue(diff.shape[1] > 0)
            self.assertFalse(np.any(np.isnan(diff)))
            self.assertTrue(is_numeric_array(diff))
            self.assertTrue(diff.shape[2] == 4)
            # self.assertTrue(diff.shape[3] == 1)

    def test_diff_optic_flow_memory(self):
        """
        this test checks the function diff_optic_flow works
        correctly for the parameter memory.
        it checks if correct errors are raised for:
        - memory containing nans
        - memory has wrong dimension

        and checks if the returned frame is correct:
        - has correct shape
        - does not contain nans
        - contains only numeric values
        """
        curr = self.mydb.scene(rowid=1)
        mem = self.mydb.scene(rowid=2)
        mem2 = curr.copy()
        mem2[3, 5, 2] = np.nan
        mem3 = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        mem3 = [mem3, mem3, mem3]
        mem3 = np.array(mem3)
        mem4 = np.zeros((3, 4, 5))

        with self.assertRaises(ValueError):
            comparing.diff_optic_flow(curr, mem2)
        with self.assertRaises(Exception):
            comparing.diff_optic_flow(curr, mem3)
        with self.assertRaises(Exception):
            comparing.diff_optic_flow(curr, mem4)

        # should be working -> check if result is correct
        for s in [mem]:
            vec = comparing.diff_optic_flow(curr, s)
            self.assertFalse(vec.shape[1] == (1, 2))
            self.assertFalse(np.any(np.isnan(vec)))
            self.assertTrue(is_numeric_array(vec))

    def test_diff_optic_flow_curr(self):
        """
        this test checks the function diff_optic_flow works
        correctly for the parameter current.
        it checks if correct errors are raised for:
        - memory containing nans
        - memory has wrong dimension

        and checks if the returned frame is correct:
        - has correct shape
        - does not contain nans
        - contains only numeric values
        """
        curr = self.mydb.scene(rowid=1)
        mem = self.mydb.scene(rowid=2)
        curr2 = curr.copy()
        curr2[3, 5, 2] = np.nan
        curr3 = [[1, 2], [1, 2], [1, 2]]
        curr3 = [curr3, curr3, curr3]
        curr3 = np.array(curr3)
        curr4 = np.zeros((3, 4, 5, 1))

        with self.assertRaises(ValueError):
            comparing.diff_optic_flow(curr2, mem)
        with self.assertRaises(Exception):
            comparing.diff_optic_flow(curr3, mem)
        with self.assertRaises(Exception):
            comparing.diff_optic_flow(curr4, mem)

        # should be working -> check if result is correct
        for s in [mem]:
            vec = comparing.diff_optic_flow(s, curr)
            self.assertFalse(vec.shape[1] == (1, 2))
            self.assertFalse(np.any(np.isnan(vec)))
            self.assertTrue(is_numeric_array(vec))


if __name__ == '__main__':
    unittest.main()
