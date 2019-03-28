"""
 Unittesting under blender
"""
import unittest
import numpy as np
from navipy.sensors.renderer import BlenderRender


class TestBlenderRender_api(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.cyberbee = BlenderRender()

    def test_class_assigments_error(self):
        """ Test that error are correctly raised
        List of tested function:
        * camera_rotation_mode
        * cycle_samples
        * camera_fov
        * camera_gaussian_width
        * camera_resolution
        """
        with self.assertRaises(TypeError):
            # Should be an integer
            self.cyberbee.cycle_samples = 0.1
        with self.assertRaises(TypeError):
            # Should be a tuple list or np.ndarray
            self.cyberbee.camera_fov = 'bla'
        with self.assertRaises(TypeError):
            # Should be a float or int, so not a complex
            self.cyberbee.camera_gaussian_width = 4 + 4j
        with self.assertRaises(TypeError):
            # Should be a tuple, list or nd.array
            self.cyberbee.camera_resolution = 'bla'

    def test_class_assigments(self):
        """ Test set/get match

        * camera_rotation_mode
        * cycle_samples
        * camera_fov
        * camera_gaussian_width
        * camera_resolution
        """
        # camera cycle_samples
        val = 100
        self.cyberbee.cycle_samples = val
        self.assertEqual(val, self.cyberbee.cycle_samples)
        # camera fov
        val = np.array([[-90, 90], [-180, 180]])
        self.cyberbee.camera_fov = val
        np.testing.assert_allclose(val, self.cyberbee.camera_fov)
        # camera gaussian
        val = 1.5
        self.cyberbee.gaussian_width = val
        self.assertEqual(val, self.cyberbee.gaussian_width)
        # camera resolution
        val = np.array([360, 180])
        self.cyberbee.camera_resolution = val
        np.testing.assert_allclose(val, self.cyberbee.camera_resolution)
