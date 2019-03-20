import inspect
import math
import os
import unittest

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.calibration.rotation_scaler import RotationScaler


class RotationScalerTest(unittest.TestCase):
    def setUp(self):
        self.dir_name = os.path.dirname(inspect.getfile(RotationScalerTest))
        self.filename = os.path.join(self.dir_name, 'rotation_calibration.json')
        self.h = math.sqrt(0.5)

    def test_applies_initial_scaling_factors(self):
        # Pitch 180 around y
        scaler = RotationScaler(Quaternion(0, 0, 1, 0))
        result = scaler.scale(Data(Vector([3, 2, 1]), 123))
        self.assertEqual(result, Data(Vector([-3, 2, -1]), 123))

    def test_load_calibration(self):
        scaler = RotationScaler(Quaternion.identity())
        scaler.load(self.filename)
        self.assertEqual(Quaternion(self.h, 0, -self.h, 1), scaler._rotation)

    def test_save_calibration(self):
        scaler = RotationScaler(Quaternion(self.h, 0, -self.h, 1))
        filename = os.path.join(self.dir_name, 'saved_rotation_calibration.json')
        # Act
        scaler.save(filename)
        # Assert
        with open(filename) as reader:
            json = reader.read()
        self.assertEqual('{"rotation":{"w":0.7071067811865476, "i":0, "j":-0.7071067811865476, "k":1}}', json)


if __name__ == '__main__':
    unittest.main()

