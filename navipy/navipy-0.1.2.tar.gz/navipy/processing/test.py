import unittest
import numpy as np
from navipy import database as database
from navipy.processing import pcode
from navipy.scene import is_numeric_array
from navipy import unittestlogger
import pkg_resources


class TestCase(unittest.TestCase):
    def setUp(self):
        unittestlogger()
        self.mydb_filename = pkg_resources.resource_filename(
            'navipy', 'resources/database.db')
        self.mydb = database.DataBase(self.mydb_filename, mode='r')

    def test_scene_posorient(self):
        """
        this test checks that the correct errors are raised if
        wrong values for the input parameters are passed to the
        function scene of the navipy.database module
        it also contains some test where correct parameter values
        were passed to the scene function and the output was
        checked for correctness.
        test cases:
        missing entries in the posorient pd.series
        None, NaN values in the posorient pd.series
        posorient is of wrong type (dictionary instead of pd.series)
        empty posorient pd.series
        """
        posorients = self.mydb.posorients
        posorient = posorients.loc[13, :]
        image = self.mydb.scene(posorient=posorient)
        self.assertIsNotNone(image)
        self.assertFalse(sum(image.shape) == 0)
        # print("shape",image.shape)
        self.assertTrue(len(image.shape) == 4)
        self.assertTrue(image.shape[3] == 1)

        # incorrect case missing column
        posorient2 = posorients.loc[13, :]
        posorient2.drop(('location', 'x'), inplace=True)
        with self.assertRaises(Exception):
            image = self.mydb.scene(posorient=posorient2)

        # incorrect case None
        posorient2 = posorients.loc[13, :]
        posorient2['location']['x'] = None
        with self.assertRaises(ValueError):
            image = self.mydb.scene(posorient=posorient2)

        # incorrect case nan
        posorient2 = posorients.loc[13, :]
        posorient2['location']['x'] = np.nan
        with self.assertRaises(ValueError):
            image = self.mydb.scene(posorient=posorient2)

        # incorrect case no pandas series but dict
        posorient2 = {}
        with self.assertRaises(TypeError):
            image = self.mydb.scene(posorient=posorient2)

        # not working case empty
        posorient2 = posorients.loc[13, :] * np.nan
        with self.assertRaises(Exception):
            image = self.mydb.scene(posorient=posorient2)

    def test_skyline_scene(self):
        """
        this test checks that the correct errors are raised if
        wrong values for the input parameters are passed to the
        function skyline_scene of the navipy.database module
        it also contains some test where correct parameter values
        were passed to the scene function and the output was
        checked for correctness.
        test cases:
        None, NaN values in the the scene
        scene is of wrong type (np.array)
        scene is of wrong size
        """
        scene = self.mydb.scene(rowid=1)
        scene2 = scene.copy()
        scene2[3, 5, 2, 0] = np.nan
        scene3 = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        scene3 = [scene3, scene3, scene3]
        scene3 = np.array(scene3)
        scene4 = np.zeros((3, 4, 5, 0))

        # contains nan
        with self.assertRaises(ValueError):
            pcode.skyline(scene2)
        # np.array instead of
        with self.assertRaises(TypeError):
            pcode.skyline(scene3)
        # wrong size
        with self.assertRaises(Exception):
            pcode.skyline(scene4)

        # should be working -> check if result(skyline) is correct
        for s in [scene]:
            skyline = pcode.skyline(s)
            self.assertFalse(skyline.shape[1] <= 0)
            self.assertTrue(skyline.shape[2] == 4)
            self.assertFalse(np.any(np.isnan(skyline)))
            # self.assertFalse(np.any(np.isNone(skyline)))
            self.assertTrue(is_numeric_array(skyline))
            self.assertTrue(skyline.shape[3] == 1)
            self.assertTrue(skyline.shape[0] > 0)
            self.assertTrue(skyline.shape[1] > 0)

    def test_id(self):
        """
        this test checks that the correct errors are raised if
        wrong values for the input parameters id of the
        function scene of the navipy.database module
        it also contains some test where correct parameter values
        were passed to the scene function and the output was
        checked for correctness.
        test cases:
        zero and negative id
        char for the id
        None for the id
        NaN for the id
        float for the id
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

        # working cases
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

    def test_distance_channel(self):
        """
        this test checks that the correct errors are raised if
        wrong values for the input parameters distance_channel is passed to the
        function scene of the navipy.database module
        it also contains some test where correct parameter values
        were passed to the scene function and the output was
        checked for correctness.
        test cases:
        None, NaN, float, char values in the for the distance channel
        negative int for the distance channel
        """
        scene = self.mydb.scene(rowid=1)

        # should not be working
        for d in ['g', None, np.nan, 8.4]:
            with self.assertRaises(TypeError):
                pcode.contrast_weighted_nearness(scene,
                                                 distance_channel=d)
        with self.assertRaises(ValueError):
            pcode.contrast_weighted_nearness(scene,
                                             distance_channel=-1)

        # should work
        d = 3
        weighted_scene = \
            pcode.contrast_weighted_nearness(scene,
                                             distance_channel=d)
        # print("last channel",d)
        self.assertTrue(is_numeric_array(weighted_scene))
        self.assertTrue(~np.any(np.isnan(weighted_scene)))
        self.assertEqual(weighted_scene.shape, scene.shape)

    def test_contr_weight_scene(self):
        """
        this test checks that the correct errors are raised if
        wrong values for the input parameter scene is passed to the
        function contr_weight_scene of the navipy.database module
        it also contains some test where correct parameter values
        were passed to the scene function and the output was
        checked for correctness.
        test cases:
        None, NaN values in the the scene
        scene is of wrong type (np.array)
        scene is of wrong size
        """
        scene = self.mydb.scene(rowid=1)

        # working cases
        contrast = pcode.contrast_weighted_nearness(scene)
        self.assertIsNotNone(contrast)
        self.assertFalse(sum(contrast.shape) == 0)
        self.assertTrue(len(contrast.shape) == 4)
        self.assertFalse(np.any(np.isnan(contrast)))
        self.assertTrue(contrast.shape[3] == 1)
        self.assertTrue(contrast.shape[2] == 4)
        self.assertTrue(contrast.shape[0] > 0)
        self.assertTrue(contrast.shape[1] > 0)

        # not working case
        scene2 = scene.copy()
        scene2[3, 2, 1, 0] = np.nan
        scene3 = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        scene3 = [scene3, scene3, scene3]
        scene3 = np.array(scene3)
        scene4 = np.zeros((3, 4, 5, 0))
        with self.assertRaises(ValueError):
            contrast = pcode.contrast_weighted_nearness(scene2)
        with self.assertRaises(Exception):
            contrast = pcode.contrast_weighted_nearness(scene3)
        with self.assertRaises(Exception):
            contrast = pcode.contrast_weighted_nearness(scene4)

    def test_contr_weight_contrast(self):
        """
        this test checks that the correct errors are raised if
        wrong values for the input parameter contrast_size are passed to the
        function skyline_scene of the navipy.database module.
        correct values are in the range between 2 and 5.
        it also contains some test where correct parameter values
        were passed to the scene function and the output was
        checked for correctness.
        test cases:
        None, NaN values, chars, floats for the contrast_size
        int values that are out of range (<2;>5)
        """
        scene = self.mydb.scene(rowid=1)
        for size in [9.4, 'g', None, np.nan]:
            with self.assertRaises(TypeError):
                contrast = pcode.contrast_weighted_nearness(
                    scene, contrast_size=size)
        for size in [8, 1, 0, -4]:
            with self.assertRaises(ValueError):
                contrast = \
                    pcode.contrast_weighted_nearness(
                        scene, contrast_size=size)

        # working cases
        for size in [2, 3, 4, 5]:
            contrast = pcode.contrast_weighted_nearness(scene,
                                                        contrast_size=size)
            self.assertIsNotNone(contrast)
            self.assertFalse(sum(contrast.shape) == 0)
            self.assertTrue(len(contrast.shape) == 4)
            self.assertFalse(np.any(np.isnan(contrast)))
            self.assertEqual(contrast.shape[3], 1)
            self.assertEqual(contrast.shape[2], scene.shape[2])
            self.assertEqual(contrast.shape[0], scene.shape[0])
            self.assertEqual(contrast.shape[1], scene.shape[1])

    def test_pcv(self):
        """
        this test checks that the correct errors are raised if
        wrong values for the input parameter direction is passed to the
        function pcv of the navipy.database module.
        correct values are in the range between 2 and 5.
        it also contains some test where correct parameter values
        were passed to the scene function and the output was
        checked for correctness.
        test cases:
        wrong shape (must match the scenes shape)
        last dimension shape does not match (must 2, azimuth, elevation)
        direction has too many dimensions
        is empty
        contains wrong values (None, nan)
        """
        # working case
        rowid = 1
        my_scene = self.mydb.scene(rowid=rowid)
        directions = self.mydb.viewing_directions.copy()
        directions = np.radians(directions)
        my_pcv = pcode.pcv(my_scene, directions)
        self.assertIsNotNone(my_pcv)
        self.assertFalse(sum(my_pcv.shape) == 0)
        self.assertTrue(len(my_pcv.shape) == 4)
        self.assertFalse(np.any(np.isnan(my_pcv)))
        self.assertTrue(my_pcv.shape[3] == 3)
        self.assertTrue(my_pcv.shape[2] == 4)
        self.assertTrue(my_pcv.shape[0] > 0)
        self.assertTrue(my_pcv.shape[1] > 0)

        # not working cases doesnt match with shape of place code
        testdirection = np.zeros((2, 4, 2))
        with self.assertRaises(Exception):
            my_pcv = pcode.pcv(my_scene, testdirection)

        # not working cases wrong last dimension
        testdirection = np.zeros((180, 360, 1))
        with self.assertRaises(Exception):
            my_pcv = pcode.pcv(my_scene, testdirection)

        # not working cases too many dimensions
        testdirection = np.zeros((180, 360, 2, 4))
        with self.assertRaises(Exception):
            my_pcv = pcode.pcv(my_scene, testdirection)

        # not working cases empty
        testdirection = np.zeros(())
        with self.assertRaises(Exception):
            my_pcv = pcode.pcv(my_scene, testdirection)

        # not working cases nans
        testdirection = np.zeros((180, 360, 2, 4))
        testdirection[2, 3, 0] = np.nan
        with self.assertRaises(ValueError):
            my_pcv = pcode.pcv(my_scene, testdirection)

        # test if error is throught for elevation or azimuth out of range
        # check elevation, should be in [-pi*2;pi*2]
        testdirections = np.zeros((180, 360, 2))
        testdirections[10, 15, 0] = -np.pi * 2 - 0.001
        with self.assertRaises(ValueError):
            my_pcv = pcode.pcv(my_scene, testdirections)

        testdirections = np.zeros((180, 360, 2))
        testdirections[10, 15, 0] = np.pi * 2 + 0.001
        with self.assertRaises(ValueError):
            my_pcv = pcode.pcv(my_scene, testdirections)

        # check azimuth, should be in [-2*pi;2*pi]
        testdirections = np.zeros((180, 360, 2))
        testdirections[10, 15, 1] = -2 * np.pi - 0.001
        with self.assertRaises(ValueError):
            my_pcv = pcode.pcv(my_scene, testdirections)

        testdirections = np.zeros((180, 360, 2))
        testdirections[10, 15, 1] = 2 * np.pi + 0.001
        with self.assertRaises(ValueError):
            my_pcv = pcode.pcv(my_scene, testdirections)

        testdirections = np.zeros((180, 360, 2))
        testdirections[10, 15, 1] = np.pi + 0.001
        testdirections[10, 16, 1] = - np.pi - 0.001
        with self.assertRaises(ValueError):
            my_pcv = pcode.pcv(my_scene, testdirections)

    def test_apcv(self):
        """
        this test checks that the correct errors are raised if
        wrong values for the input parameter direction is passed to the
        function apcv of the navipy.database module.
        correct values are in the range between 2 and 5.
        it also contains some test where correct parameter values
        were passed to the scene function and the output was
        checked for correctness.
        test cases:
        wrong shape (must match the scenes shape)
        last dimension shape does not match (must 2, azimuth, elevation)
        direction has too many dimensions
        is empty
        contains wrong values (None, nan)
        """
        # working case
        rowid = 1
        my_scene = self.mydb.scene(rowid=rowid)
        directions = self.mydb.viewing_directions.copy()
        directions = np.radians(directions)

        my_pcv = pcode.apcv(my_scene, directions)

        self.assertIsNotNone(my_pcv)
        self.assertFalse(sum(my_pcv.shape) == 0)
        self.assertTrue(len(my_pcv.shape) == 4)
        self.assertFalse(np.any(np.isnan(my_pcv)))
        self.assertTrue(my_pcv.shape[3] == 3)
        self.assertTrue(my_pcv.shape[2] == 4)
        self.assertTrue(my_pcv.shape[0] == 1)
        self.assertTrue(my_pcv.shape[1] == 1)

        # not working cases doesnt match with shape of place code
        testdirection = np.zeros((2, 4, 2))
        with self.assertRaises(Exception):
            my_pcv = pcode.apcv(my_scene, testdirection)

        # not working cases wrong last dimension
        testdirection = np.zeros((180, 360, 1))
        with self.assertRaises(Exception):
            my_pcv = pcode.apcv(my_scene, testdirection)

        # not working cases too many dimensions
        testdirection = np.zeros((180, 360, 2, 4))
        with self.assertRaises(Exception):
            my_pcv = pcode.apcv(my_scene, testdirection)

        # not working cases empty
        testdirection = np.zeros(())
        with self.assertRaises(Exception):
            my_pcv = pcode.apcv(my_scene, testdirection)

        # not working cases nans
        testdirection = np.zeros((180, 360, 2, 4))
        testdirection[2, 3, 0] = np.nan
        with self.assertRaises(ValueError):
            my_pcv = pcode.apcv(my_scene, testdirection)

    def test_size(self):
        """
        this test checks that the correct errors are raised if
        wrong values for the input parameter size are passed to the
        function michelson_contrast of the navipy.database module.
        correct values are in the range between 2 and 5.
        it also contains some test where correct parameter values
        were passed to the scene function and the output was
        checked for correctness.
        test cases:
        None, NaN values, chars, floats for the contrast_size
        int values that are out of range (<2;>5)
        """
        scene = self.mydb.scene(rowid=1)
        scene2 = scene.copy()
        scene2[3, 5, 2, 0] = np.nan
        scene3 = [[1, 2, 3,4], [1, 2, 3,4], [1, 2, 3, 4],[1,2,3, 4]]
        scene3 = [scene3, scene3, scene3,scene3]
        scene3 = np.array(scene3)
        scene4 = np.zeros((3, 4, 5, 0))
        with self.assertRaises(ValueError):
            pcode.michelson_contrast(scene2)
        # np.array instead of
        with self.assertRaises(TypeError):
            pcode.michelson_contrast(scene3)
        # wrong size
        with self.assertRaises(Exception):
            pcode.michelson_contrast(scene4)

        with self.assertRaises(TypeError):
            pcode.contrast_weighted_nearness(scene3)


        for size in [8, 1, 0, -4]:
            with self.assertRaises(ValueError):
                contrast = pcode.michelson_contrast(
                    scene, size=size)
        for size in [9.4, 'g', None, np.nan]:
            with self.assertRaises(TypeError):
                contrast = pcode.michelson_contrast(
                    scene, size=size)

        # working cases
        for size in [2, 3, 4, 5]:
            contrast = pcode.michelson_contrast(scene, size=size)
            self.assertIsNotNone(contrast)
            self.assertFalse(sum(contrast.shape) == 0)
            self.assertTrue(len(contrast.shape) == 4)
            self.assertFalse(np.any(np.isnan(contrast)))
            self.assertTrue(contrast.shape[3] == 1)
            self.assertTrue(contrast.shape[2] == 4)
            self.assertTrue(contrast.shape[0] > 0)
            self.assertTrue(contrast.shape[1] > 0)

    def test_michelsoncontrast_scene(self):
        """
        this test checks that the correct errors are raised if
        wrong values for the input parameter scene is passed to the
        function michelson_contrast of the navipy.database module
        it also contains some test where correct parameter values
        were passed to the scene function and the output was
        checked for correctness.
        test cases:
        None, NaN values in the the scene
        scene is of wrong type (np.array)
        scene is of wrong size
        """

        scene = self.mydb.scene(rowid=1)

        # working cases
        contrast = pcode.michelson_contrast(scene)
        self.assertIsNotNone(contrast)
        self.assertFalse(sum(contrast.shape) == 0)
        self.assertTrue(len(contrast.shape) == 4)
        self.assertFalse(np.any(np.isnan(contrast)))
        self.assertTrue(contrast.shape[3] == 1)
        self.assertTrue(contrast.shape[2] == 4)
        self.assertTrue(contrast.shape[0] > 0)
        self.assertTrue(contrast.shape[1] > 0)

        # not working case
        scene2 = scene.copy()
        scene2[3, 2, 1, 0] = np.nan
        scene3 = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        scene3 = [scene3, scene3, scene3]
        scene3 = np.array(scene3)
        scene4 = np.zeros((3, 4, 5, 0))
        for s in [scene2, scene3, scene4]:
            with self.assertRaises(Exception):
                contrast = pcode.michelson_contrast(s,)


if __name__ == '__main__':
    unittest.main()
