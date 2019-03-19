import unittest

from rover_position_rjg.csv_helpers.quaternion_csv_converter import *


class TestQuaternionCsvConverter(unittest.TestCase):
    def test_convert_quaternion_to_csv(self):
        converter = QuaternionCsvConverter()
        row = converter.to_row(Quaternion(7.7, 1.1, 2.2, 3.3))
        self.assertEqual([7.7, 1.1, 2.2, 3.3], row)

    def test_row_to_quaternion(self):
        converter = QuaternionCsvConverter()
        quaternion = converter.to_object([1.2, 3.4, 5.6, 6.7])
        self.assertEqual(Quaternion(1.2, 3.4, 5.6, 6.7), quaternion)
