import unittest

from rover_position_rjg.csv_helpers.position_csv_converter import PositionCsvConverter
from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.position.position import Position


class TestPositionCsvConverter(unittest.TestCase):
    def test_convert_to_csv(self):
        converter = PositionCsvConverter()
        acceleration = Vector([1.2, 3.4, 5.6])
        velocity = Vector([7.8, 8.9, 9.1])
        coordinates = Vector([-1, -2, -3])
        attitude = Quaternion(1, 2, 3, 4)
        row = converter.to_row(Position(attitude, acceleration, velocity, coordinates))
        self.assertEqual([1, 2, 3, 4, 1.2, 3.4, 5.6, 7.8, 8.9, 9.1, -1, -2, -3], row)

    def test_convert_to_csv_no_attitude(self):
        converter = PositionCsvConverter()
        acceleration = Vector([1.2, 3.4, 5.6])
        velocity = Vector([7.8, 8.9, 9.1])
        coordinates = Vector([-1, -2, -3])
        row = converter.to_row(Position(None, acceleration, velocity, coordinates))
        self.assertEqual([None, None, None, None, 1.2, 3.4, 5.6, 7.8, 8.9, 9.1, -1, -2, -3], row)

    def test_row_to_object(self):
        converter = PositionCsvConverter()
        output = converter.to_object([1, 2, 3, 4, 1.2, 3.4, 5.6, 7.8, 8.9, 9.1, -1, -2, -3])
        self.assertEqual(Quaternion(1, 2, 3, 4), output.attitude)
        self.assertEqual(Vector([1.2, 3.4, 5.6]), output.acceleration)
        self.assertEqual(Vector([7.8, 8.9, 9.1]), output.velocity)
        self.assertEqual(Vector([-1, -2, -3]), output.position)

    def test_row_to_object_no_attitude(self):
        converter = PositionCsvConverter()
        output = converter.to_object([None, None, None, None, 1.2, 3.4, 5.6, 7.8, 8.9, 9.1, -1, -2, -3])
        self.assertEqual(None, output.attitude)
        self.assertEqual(Vector([1.2, 3.4, 5.6]), output.acceleration)
        self.assertEqual(Vector([7.8, 8.9, 9.1]), output.velocity)
        self.assertEqual(Vector([-1, -2, -3]), output.position)
