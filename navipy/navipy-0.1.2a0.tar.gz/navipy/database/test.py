import unittest
import sqlite3
import numpy as np
import pandas as pd
from navipy import database
# from navipy.processing.tools import is_numeric_array
import pkg_resources
import tempfile
from navipy.database import DataBase
from navipy import unittestlogger


class TestCase(unittest.TestCase):
    def setUp(self):
        unittestlogger()
        self.mydb_filename = pkg_resources.resource_filename(
            'navipy', 'resources/database2.db')
        self.mydb = DataBase(self.mydb_filename, mode='r')

    def test_DataBase_init_(self):
        """
        this test checks the initialization of a DataBase works
        correctly.
        it checks if correct errors are raised for:
        - a database file with out .db ending is used for initialization
        - wrong types are passed for the database name
        i.e. integers, floats, none, nan
        """
        # filename must end with .db
        with self.assertRaises(NameError):
            DataBase('test')
        # filename must be string
        for n in [2, 5.0, None, np.nan]:
            with self.assertRaises(TypeError):
                DataBase(n)

        # only works if testdb was created before e.g. with DataBase
        # with self.assertRaises(NameError):
        #    DataBase('test')

    def test_DataBase_init_channel(self):
        """
        this test checks the initialization of a DataBase works
        correctly.
        it checks if correct errors are raised for:
        - channels names, which are no strings or chars
        - channel name is None value or nan
        """
        # channels must be strings or char
        for n in [3, 8.7, None, np.nan]:
            with self.assertRaises(TypeError):
                DataBase(self.mydb_filename, channels=n)
        with self.assertRaises(ValueError):
            DataBase(self.mydb_filename, channels=[None, 2])

    def test_table_exist(self):
        """
        this test checks if the function table_exists works correctly
        it checks if correct errors are raised for:
        - a database name that are not of type string or char
        i.e. integer, float, none, nan
        - Attention: in this test the check for a table that existed
        did not work correctly (False was returned)
        """
        # self.assertFalse(self.mydb.table_exist('testblubb'))
        for n in [2, 7.0, None, np.nan]:
            with self.assertRaises(TypeError):
                self.assertFalse(self.mydb.table_exist(n))
        # self.assertFalse(self.mydb.table_exist(self.mydb_filename))

    def test_check_data_validity(self):
        """
        this test checks the function data validity works
        correctly. It should return true if the database
        contains data in the row, that is checked for
        it checks if correct errors are raised for:
        - row numbers that are not integers.
        i.e. float non, nan (must be integer)
        - row is out of range; smaller or equal to 0
        - checks if true is returned for an exiting entry (row=1)
        """
        for n in [7.0, None, np.nan]:
            with self.assertRaises(TypeError):
                self.mydb.check_data_validity(n)
        for n in [-1, 0]:
            with self.assertRaises(ValueError):
                self.mydb.check_data_validity(n)
        assert self.mydb.check_data_validity(1)

    def test_read_posorient(self):
        """
        this test checks the function read_posorient works
        correctly.
        it checks if correct errors are raised for:
        - posorient is missing an entry (no 'x' column)
        - posorient contains nan or none values
        - posorient is of wrong type (dict instead of pd.series)
        """
        posorient = self.mydb.read_posorient(rowid=1)
        posid = self.mydb.read_posorient(posorient=posorient)
        # print(posid)
        assert posid['location']['x'] == posorient['location']['x']

        # incorrect case missing column
        posorient2 = posorient.copy()
        posorient2 = posorient2.drop('x', level=1)
        posorient2['location']['x'] = np.nan
        with self.assertRaises(ValueError):
            self.mydb.read_posorient(posorient=posorient2)

        # incorrect case None
        posorient2 = posorient.copy()
        posorient2['location']['x'] = None
        with self.assertRaises(ValueError):
            self.mydb.read_posorient(posorient=posorient2)

        # incorrect case nan
        posorient2 = posorient.copy()
        posorient2['location']['x'] = np.nan
        with self.assertRaises(ValueError):
            self.mydb.read_posorient(posorient=posorient2)

        # incorrect case no pandas series but dict
        posorient2 = posorient.to_dict()
        with self.assertRaises(TypeError):
            self.mydb.read_posorient(posorient=posorient2)

        # not working case empty
        tuples = [('location', 'x'), ('location', 'y'),
                  ('location', 'z'), ('xyz', 'alpha_0'),
                  ('xyz', 'alpha_1'), ('xyz', 'alpha_2')]
        index = pd.MultiIndex.from_tuples(tuples,
                                          names=['position', 'orientation'])

        posorient2 = pd.Series(index=index)
        with self.assertRaises(Exception):
            self.mydb.read_posorient(posorient=posorient2)

    def test_read_posid_id(self):
        """
        this test checks the function read_posorient works
        correctly.
        it checks if correct errors are raised for:
        - rowid is out of range (<=0)
        - rowid is of type char, none, nan, float
        and checks if the returned entry for rowid 1 is correct
        - that it all columns and correct values
        """
        posorient = self.mydb.posorients.iloc[0, :]
        for rowid in [0, -2]:
            with self.assertRaises(ValueError):
                self.mydb.read_posorient(rowid=rowid)
        with self.assertRaises(TypeError):
            self.mydb.read_posorient(rowid='T')
        with self.assertRaises(Exception):
            self.mydb.read_posorient(rowid=None)
        with self.assertRaises(TypeError):
            self.mydb.read_posorient(rowid=np.nan)
        with self.assertRaises(TypeError):
            self.mydb.read_posorient(rowid=4.5)

        for rowid in [1]:
            posoriend2 = self.mydb.read_posorient(rowid=rowid)
            pd.testing.assert_series_equal(posoriend2, posorient)

    def test_scene_id(self):
        """
        this test checks the function scene works
        correctly.
        it checks if correct errors are raised for:
        - rowid is out of range (<=0)
        - rowid is of type char, none, nan, float

        and checks if the returned entry for different
        rows is correct
        - has correct shape
        - does not contain nans
        """
        for rowid in [0, -2]:
            with self.assertRaises(ValueError):
                # print("rowid",rowid)
                self.mydb.scene(rowid=rowid)
        with self.assertRaises(TypeError):
            self.mydb.scene(rowid='T')
        with self.assertRaises(Exception):
            self.mydb.scene(rowid=None)
        with self.assertRaises(TypeError):
            self.mydb.scene(rowid=np.nan)
        with self.assertRaises(TypeError):
            self.mydb.scene(rowid=4.5)

        for rowid in [1, 2, 3, 4, 5]:
            image = self.mydb.scene(rowid=rowid)
            # image=np.array(image)
            self.assertIsNotNone(image)
            self.assertFalse(sum(image.shape) == 0)
            self.assertTrue(len(image.shape) == 4)
            self.assertFalse(np.any(np.isnan(image)))
            self.assertTrue(image.shape[3] == 1)
            self.assertTrue(image.shape[2] == 4)
            self.assertTrue(image.shape[0] > 0)
            self.assertTrue(image.shape[1] > 0)

    def test_scene_posorient(self):
        """
        this test checks the function scene works
        correctly.
        it checks if correct errors are raised for:
        - posorient is missing an entry (no 'x' column)
        - posorient contains nan or none values
        - posorient is of wrong type (dict instead of pd.series)
        """
        posorient = self.mydb.posorients.iloc[0, :]
        posorient.name = 1
        image = self.mydb.scene(posorient=posorient)
        self.assertIsNotNone(image)
        self.assertFalse(sum(image.shape) == 0)
        # print("shape",image.shape)
        self.assertTrue(len(image.shape) == 4)
        self.assertTrue(image.shape[3] == 1)

        # incorrect case missing column
        posorient2 = posorient.copy()
        posorient2 = posorient2.drop(('location', 'x'))
        with self.assertRaises(Exception):
            image = self.mydb.scene(posorient=posorient2)

        # incorrect case None
        posorient2 = posorient.copy()
        posorient2['location']['x'] = None
        with self.assertRaises(ValueError):
            image = self.mydb.scene(posorient=posorient2)

        # incorrect case nan
        posorient2 = posorient.copy()
        posorient2['location']['x'] = np.nan
        with self.assertRaises(ValueError):
            image = self.mydb.scene(posorient=posorient2)

        # incorrect case no pandas series but dict
        posorient2 = posorient.to_dict()
        with self.assertRaises(TypeError):
            image = self.mydb.scene(posorient=posorient2)

        # not working case empty
        posorient2 = pd.Series(index=posorient.index)
        with self.assertRaises(Exception):
            image = self.mydb.scene(posorient=posorient2)

    def test_denormalise_image(self):
        """
        this test checks the function denormalise_image works
        correctly.
        it checks if correct errors are raised for:
        - image has wrong type (list instead of np.ndarray)
        - image does not have enough dimensions
        - image contains nan values
        - image has to many dimensions
        - cminmax range is missing one channel
        - cminmax range is empty pd.series
        - cminmax range is dictionary
        - cminmax contains nans
        """
        image = self.mydb.scene(rowid=1)
        image = np.squeeze(image)
        cminmaxrange = pd.Series(index=['R_min', 'R_max', 'R_range',
                                        'G_min', 'G_max', 'G_range',
                                        'B_min', 'B_max', 'B_range',
                                        'D_min', 'D_max', 'D_range'])
        cminmaxrange.R_min = 0
        cminmaxrange.R_max = 1
        cminmaxrange.R_range = 1
        cminmaxrange.G_min = 0
        cminmaxrange.G_max = 1
        cminmaxrange.G_range = 1
        cminmaxrange.B_min = 0
        cminmaxrange.B_max = 1
        cminmaxrange.B_range = 1
        cminmaxrange.D_min = 0
        cminmaxrange.D_max = 1
        cminmaxrange.D_range = 1
        imagecorrect = (image.copy() * 500).astype(int)
        self.mydb.denormalise_image(imagecorrect, cminmaxrange)

        # not working
        image2 = image.copy().tolist()
        with self.assertRaises(TypeError):
            self.mydb.denormalise_image(image2, cminmaxrange)

        image2 = image[:, :, 0].copy()
        with self.assertRaises(Exception):
            self.mydb.denormalise_image(image2, cminmaxrange)

        image2 = image.copy()
        image2[23, 34, 0] = np.nan
        with self.assertRaises(ValueError):
            self.mydb.denormalise_image(image2, cminmaxrange)

        # image2 = image
        # image2[23,34,0] = 'addsf'
        # with self.assertRaises(ValueError):
        #    denormed=self.mydb.denormalise_image(image2,cminmaxrange)

        image2 = image[np.newaxis, :, :, :]
        with self.assertRaises(Exception):
            self.mydb.denormalise_image(image2, cminmaxrange)

        cminmaxrange2 = pd.Series(index=['R_min', 'R_max', 'R_range',
                                         'B_min', 'B_max', 'B_range',
                                         'D_min', 'D_max', 'D_range'])
        cminmaxrange2.R_min = 0
        cminmaxrange2.R_max = 1
        cminmaxrange2.R_range = 1
        cminmaxrange2.B_min = 0
        cminmaxrange2.B_max = 1
        cminmaxrange2.B_range = 1
        cminmaxrange2.D_min = 0
        cminmaxrange2.D_max = 1
        cminmaxrange2.D_range = 1
        imagecorrect = (image.copy() * 500).astype(int)
        with self.assertRaises(ValueError):
            self.mydb.denormalise_image(imagecorrect, cminmaxrange2)

        cminmaxrange3 = pd.Series(index=['R_min', 'R_max', 'R_range',
                                         'G_min', 'G_max', 'G_range',
                                         'B_min', 'B_max', 'B_range',
                                         'D_min', 'D_max', 'D_range'])
        # cminmaxrange3.R_min = []
        # cminmaxrange3.R_max = []
        # cminmaxrange3.R_range = []
        # cminmaxrange3.G_min = []
        # cminmaxrange3.G_max = []
        # cminmaxrange3.G_range = []
        # cminmaxrange3.B_min = []
        # cminmaxrange3.B_max = []
        # cminmaxrange3.B_range = []
        # cminmaxrange3.D_min = []
        # cminmaxrange3.D_max = []
        # cminmaxrange3.D_range = []

        with self.assertRaises(ValueError):
            self.mydb.denormalise_image(imagecorrect, cminmaxrange3)

        cminmaxrange3 = {}
        cminmaxrange3['R_min'] = 0
        cminmaxrange3['R_max'] = 1
        cminmaxrange3['R_range'] = 1
        cminmaxrange3['G_min'] = 0
        cminmaxrange3['G_max'] = 1
        cminmaxrange3['G_range'] = 1
        cminmaxrange3['B_min'] = 0
        cminmaxrange3['B_max'] = 1
        cminmaxrange3['B_range'] = 1
        cminmaxrange3['D_min'] = 0
        cminmaxrange3['D_max'] = 1
        cminmaxrange3['D_range'] = 1
        with self.assertRaises(TypeError):
            self.mydb.denormalise_image(imagecorrect, cminmaxrange3)

        cminmaxrange.R_min = np.nan
        with self.assertRaises(ValueError):
            self.mydb.denormalise_image(imagecorrect, cminmaxrange)

    def test_normalise_image(self):
        """
        this test checks the function normalise_image works
        correctly.
        it checks if correct errors are raised for:
        - image is of wrong type (list)
        - image has wrong dimensionality (too big, too small)
        - image contains nan values
        """
        image = self.mydb.scene(rowid=1)
        image = np.squeeze(image)
        with tempfile.TemporaryDirectory() as folder:
            testdb_filename = folder + '/testdatabase.db'
            loadDB = DataBase(testdb_filename, mode='w')
            loadDB.normalise_image(image)

            # not working
            image2 = image.tolist()
            with self.assertRaises(TypeError):
                loadDB.normalise_image(image2)

            image2 = image[:, :, 0].copy()
            with self.assertRaises(Exception):
                loadDB.normalise_image(image2)

            image2 = image.copy()
            image2[23, 34, 0] = np.nan
            with self.assertRaises(ValueError):
                loadDB.normalise_image(image2)

            """image2 = image.copy()
            image2[23,34,0] = 'addsf'
            with self.assertRaises(ValueError):
                denormed=loadDB.normalise_image(image2)"""

            image2 = image[np.newaxis, :, :, :].copy()
            with self.assertRaises(Exception):
                loadDB.normalise_image(image2)

    def test_insert_replace(self):
        """
        this test checks the function insert_replace works
        correctly.
        it checks if correct errors are raised for:
        - filename is of type integer, float, nan or none
        - filename does not exist in database/params are wrong
        """
        params = {}
        params['hight'] = 1.7
        params['age'] = 20
        with tempfile.TemporaryDirectory() as folder:
            testdb_filename = folder + '/testdatabase.db'
            tmpmydb = database.DataBase(testdb_filename, mode='w')

            for name in [3, 7.5, np.nan, None]:
                with self.assertRaises(TypeError):
                    tmpmydb.insert_replace(name, params)

            with self.assertRaises(sqlite3.OperationalError):
                tmpmydb.insert_replace('test', params)


if __name__ == '__main__':
    unittest.main()
