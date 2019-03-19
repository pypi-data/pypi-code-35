import unittest

from rover_position_rjg.csv_helpers.attitude_output_csv_converter import AttitudeOutputCsvConverter
from rover_position_rjg.data.flags import Flags
from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.filters.attitude_filter import AttitudeOutput


class TestAttitudeOutputCsvConverter(unittest.TestCase):
    def test_convert_to_csv(self):
        converter = AttitudeOutputCsvConverter()
        acceleration = Vector([1.2, 3.4, 5.6])
        attitude = Quaternion(1, 2, 3, 4)
        status = Flags(0xF0)
        row = converter.to_row(AttitudeOutput(acceleration, attitude, status))
        self.assertEqual([1.2, 3.4, 5.6, 1, 2, 3, 4, 0xF0], row)

    def test_row_to_object(self):
        converter = AttitudeOutputCsvConverter()
        output = converter.to_object([1.2, 3.4, 5.6, 1, 2, 3, 4, 0xF0])
        self.assertEqual(Vector([1.2, 3.4, 5.6]), output.acceleration)
        self.assertEqual(Quaternion(1, 2, 3, 4), output.attitude)
        self.assertEqual(Flags(0xF0), output.status)
