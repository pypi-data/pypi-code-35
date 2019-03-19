import inspect
import os
import unittest

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.calibration.simple_scaler import SimpleScaler


class SimpleScalerTest(unittest.TestCase):
    def setUp(self):
        dir_name = os.path.dirname(inspect.getfile(SimpleScalerTest))
        self.filename = os.path.join(dir_name, 'calibration.json')

    def test_applies_initial_scaling_factors(self):
        scaler = SimpleScaler(Vector([1, -1, 2]), Vector([2, 4, 6]))
        result = scaler.scale(Data(Vector([10, 11, 12]), 123))
        self.assertEqual(result, Data(Vector([18, 48, 60]), 123))

    def test_load_calibration(self):
        scaler = SimpleScaler(Vector([0, 0, 0]), Vector([1, 1, 1]))
        scaler.load(self.filename)
        self.assertEqual(scaler.offset, Vector([3, 6, 9]))
        self.assertEqual(scaler.multiplier, Vector([30, 20, 10]))

    def test_save_calibration(self):
        scaler = SimpleScaler(Vector([3, 6, 9]), Vector([30, 20, 10]))
        filename = 'saved_calibration.json'
        # Act
        scaler.save(filename)
        # Assert
        with open(filename) as reader:
            json = reader.read()
        self.assertEquals('{"offset":{"x":3, "y":6, "z":9}, "multiplier":{"x":30, "y":20, "z":10}}', json)


if __name__ == '__main__':
    unittest.main()

