import itertools
import unittest
from testfixtures import compare
from rover_position_rjg.sensors.imu.nine_dof_data import *
from rover_position_rjg.sensors.imu.nine_dof_data_to_csv import NineDoFDataCsvConverter


class NineDoFDataToCsvTest(unittest.TestCase):
    def setUp(self):
        self.empty = NineDoFData(None, None, None, None)
        acceleration = Data[Vector](Vector([1, 2, 3]), 100)
        angular_velocity = Data[Vector](Vector([4, 5, 6]), 101)
        magnetic_field = Data[Vector](Vector([7, 8, 9]), 102)
        temperature = Data[float](1.23, 103)
        self.partial = NineDoFData(Data[Vector](None, 100), Data[Vector](None, 101), None, None)
        self.complete = NineDoFData(acceleration, angular_velocity, magnetic_field, temperature)
        self.complete_with_zero = NineDoFData(acceleration, Data(Vector.zero(), 101), magnetic_field, temperature)
        self.converter = NineDoFDataCsvConverter()

    def test_to_row_creates_complete_row(self):
        row = self.converter.to_row(self.complete)
        self.assertEqual([1, 2, 3, 100, 4, 5, 6, 101, 7, 8, 9, 102, 1.23, 103], row)

    def test_to_row_creates_partial_row(self):
        row = self.converter.to_row(self.partial)
        self.assertEqual([None, None, None, 100, None, None, None, 101, None, None, None, None, None, None], row)

    def test_to_row_creates_empty_row(self):
        row = self.converter.to_row(self.empty)
        self.assertEqual(list(itertools.repeat(None, 14)), row)

    def test_to_object_creates_complete_object(self):
        row = [1, 2, 3, 100, 4, 5, 6, 101, 7, 8, 9, 102, 1.23, 103]
        value = self.converter.to_object(row)
        compare(value, self.complete)

    def test_to_object_creates_complete_object_with_zero_vector(self):
        row = [1, 2, 3, 100, 0, 0, 0, 101, 7, 8, 9, 102, 1.23, 103]
        value = self.converter.to_object(row)
        compare(value, self.complete_with_zero)

    def test_to_object_creates_partial_object(self):
        row = [None, None, None, 100, None, None, None, 101, None, None, None, None, None, None]
        value = self.converter.to_object(row)
        compare(value, self.partial)

    def test_to_object_creates_empty_object(self):
        row = [None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        value = self.converter.to_object(row)
        compare(value, self.empty)

    def test_round_trip(self):
        pass

    def test_round_trip_empty(self):
        pass

    def test_round_trip_partial(self):
        pass


if __name__ == '__main__':
    unittest.main()
