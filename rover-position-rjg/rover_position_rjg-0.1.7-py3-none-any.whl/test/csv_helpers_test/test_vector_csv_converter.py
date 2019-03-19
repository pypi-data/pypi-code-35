import unittest

from rover_position_rjg.csv_helpers.vector_csv_converter import *


class TestVectorCsvConverter(unittest.TestCase):
    def test_convert_vector_to_csv(self):
        converter = VectorCsvConverter()
        row = converter.to_row(Vector([1.2, 3.4, 5.6]))
        self.assertEqual([1.2, 3.4, 5.6], row)

    def test_row_to_vector(self):
        converter = VectorCsvConverter()
        vector = converter.to_object([1.2, 3.4, 5.6])
        self.assertEqual(Vector([1.2, 3.4, 5.6]), vector)

    def test_row_to_vector_2(self):
        converter = VectorCsvConverter()
        vector = converter.to_object(['1.2', '3.4', '5.6'])
        self.assertEqual(Vector([1.2, 3.4, 5.6]), vector)
