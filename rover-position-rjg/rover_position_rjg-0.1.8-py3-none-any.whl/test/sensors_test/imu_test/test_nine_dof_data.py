import unittest
from json import loads

from rover_position_rjg.data.flags import Flags
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.data.data import Data


class NineDoFDataTest(unittest.TestCase):

    def test_initialises_properties(self):
        acceleration = Data(Vector([1, 2, 3]), 1)
        angular_velocity = Data(Vector([1, 2, 3]), 2)
        magnetic_field = Data(Vector([1, 2, 3]), 3)
        temperature = Data(1.23, 4)

        data = NineDoFData(acceleration, angular_velocity, magnetic_field, temperature)

        self.assertIs(acceleration, data.acceleration)
        self.assertIs(angular_velocity, data.angular_velocity)
        self.assertIs(magnetic_field, data.magnetic_field)
        self.assertIs(temperature, data.temperature)
        self.assertEqual(0, int(data.status))

    def test_zero_gives_zero_values(self):
        zero = NineDoFData.zero()

        self.assertEqual(zero.acceleration.timestamp, 0)
        self.assertEqual(Vector.zero(), zero.acceleration.value)
        self.assertEqual(zero.angular_velocity.timestamp, 0)
        self.assertEqual(Vector.zero(), zero.angular_velocity.value)
        self.assertEqual(zero.magnetic_field.timestamp, 0)
        self.assertEqual(Vector.zero(), zero.magnetic_field.value)
        self.assertEqual(zero.temperature.value, 0)
        self.assertEqual(zero.temperature.timestamp, 0)
        self.assertEqual(0, int(zero.status))

    def test_zero_values_are_independent(self):
        zero = NineDoFData.zero()

        self.assertIsNot(zero.acceleration, zero.angular_velocity)
        self.assertIsNot(zero.acceleration, zero.magnetic_field)
        self.assertIsNot(zero.acceleration.value, zero.angular_velocity.value)
        self.assertIsNot(zero.acceleration.value, zero.magnetic_field.value)

    def test_one_gives_one_values(self):
        one = NineDoFData.one()

        v_one = Vector([1, 1, 1])
        self.assertEqual(one.acceleration.timestamp, 0)
        self.assertEqual(v_one, one.acceleration.value)
        self.assertEqual(one.angular_velocity.timestamp, 0)
        self.assertEqual(v_one, one.angular_velocity.value)
        self.assertEqual(one.magnetic_field.timestamp, 0)
        self.assertEqual(v_one, one.magnetic_field.value)
        self.assertEqual(one.temperature.value, 1)
        self.assertEqual(one.temperature.timestamp, 0)

    def test_one_values_are_independent(self):
        one = NineDoFData.one()
        self.assertIsNot(one.acceleration, one.angular_velocity)
        self.assertIsNot(one.acceleration, one.magnetic_field)
        self.assertIsNot(one.acceleration.value, one.angular_velocity.value)
        self.assertIsNot(one.acceleration.value, one.magnetic_field.value)

    def test_eq_self_and_identical_value(self):
        data1 = self.build_value()
        data2 = self.build_value()
        # Assert
        self.assertEqual(data1, data1)
        self.assertEquals(data1, data2)

    def test_not_equal_if_data_different(self):
        data = self.build_value()
        different = self.build_value()
        different.acceleration.value += Vector([1, 1, 1])
        self.assertFalse(data == different)
        different = self.build_value()
        different.angular_velocity.value += Vector([1, 1, 1])
        self.assertFalse(data == different)
        different = self.build_value()
        different.magnetic_field.value += Vector([1, 1, 1])
        self.assertFalse(data == different)
        different = self.build_value()
        different.temperature.value = 6.5
        self.assertFalse(data == different)

    def test_not_equal_if_timestamps_different(self):
        data = self.build_value()
        different = self.build_value()
        different.acceleration.timestamp += 1
        self.assertFalse(data == different)
        different = self.build_value()
        different.angular_velocity.timestamp += 1
        self.assertFalse(data == different)
        different = self.build_value()
        different.magnetic_field.timestamp += 1
        self.assertFalse(data == different)
        different = self.build_value()
        different.temperature.timestamp += 1
        self.assertFalse(data == different)

    def test_not_equal_if_status_different(self):
        data1 = self.build_value()
        data2 = self.build_value()
        data2.status[2] = True
        # Assert
        self.assertFalse(data1 == data2)

    def test_add_returns_sum(self):
        data = self.build_value()
        data2 = self.build_value()
        result = data + data2  # type: NineDoFData
        self.assertEqual(2.46, result.temperature.value)
        self.assertEqual(Vector([2, 4, 6]), result.acceleration.value)
        self.assertEqual(Vector([8, 10, 12]), result.angular_velocity.value)
        self.assertEqual(Vector([14, 16, 18]), result.magnetic_field.value)

    def test_result_of_add_has_timestamps_and_status_from_self(self):
        data = self.build_value()
        data2 = self.build_value()
        data2.acceleration.timestamp = 99
        data2.angular_velocity.timestamp = 99
        data2.magnetic_field.timestamp = 99
        data2.temperature.timestamp = 99
        data2.status = Flags(57)
        result = data + data2  # type: NineDoFData
        self.assertEqual(1, result.acceleration.timestamp)
        self.assertEqual(2, result.angular_velocity.timestamp)
        self.assertEqual(3, result.magnetic_field.timestamp)
        self.assertEqual(4, result.temperature.timestamp)
        self.assertEqual(123, int(result.status))

    def test_subtract_returns_difference(self):
        data = self.build_value()
        acceleration = Data(Vector([1, 1, 1]), 11)
        angular_velocity = Data(Vector([2, 2, 2]), 22)
        magnetic_field = Data(Vector([3, 3, 3]), 33)
        temperature = Data(0.13, 4)
        data2 = NineDoFData(acceleration, angular_velocity, magnetic_field, temperature)
        result = data - data2  # type: NineDoFData
        self.assertEqual(1.1, result.temperature.value)
        self.assertEqual(Vector([0, 1, 2]), result.acceleration.value)
        self.assertEqual(Vector([2, 3, 4]), result.angular_velocity.value)
        self.assertEqual(Vector([4, 5, 6]), result.magnetic_field.value)

    def test_result_of_subtract_has_timestamps_and_status_from_self(self):
        data = self.build_value()
        data2 = self.build_value()
        data2.acceleration.timestamp = 99
        data2.angular_velocity.timestamp = 99
        data2.magnetic_field.timestamp = 99
        data2.temperature.timestamp = 99
        data2.status = Flags(57)
        result = data - data2  # type: NineDoFData
        self.assertEqual(1, result.acceleration.timestamp)
        self.assertEqual(2, result.angular_velocity.timestamp)
        self.assertEqual(3, result.magnetic_field.timestamp)
        self.assertEqual(4, result.temperature.timestamp)
        self.assertEqual(123, int(result.status))

    def test_multiply_by_scalar(self):
        data = self.build_value()
        result: NineDoFData = data * 3
        self.assertEqual(3.69, result.temperature.value)
        self.assertEqual(Vector([3, 6, 9]), result.acceleration.value)
        self.assertEqual(Vector([12, 15, 18]), result.angular_velocity.value)
        self.assertEqual(Vector([21, 24, 27]), result.magnetic_field.value)

    def test_result_of_multiply_has_same_timestamps_and_status(self):
        data = self.build_value()
        result: NineDoFData = data * 3
        self.assertEqual(1, result.acceleration.timestamp)
        self.assertEqual(2, result.angular_velocity.timestamp)
        self.assertEqual(3, result.magnetic_field.timestamp)
        self.assertEqual(4, result.temperature.timestamp)
        self.assertEqual(123, int(result.status))

    def test_divide_by_scalar(self):
        data = self.build_value()
        result: NineDoFData = data / 2
        self.assertEqual(0.615, result.temperature.value)
        self.assertEqual(Vector([0.5, 1, 1.5]), result.acceleration.value)
        self.assertEqual(Vector([2, 2.5, 3]), result.angular_velocity.value)
        self.assertEqual(Vector([3.5, 4, 4.5]), result.magnetic_field.value)

    def test_result_of_divide_has_same_timestamps_and_status(self):
        data = self.build_value()
        result: NineDoFData = data / 3
        self.assertEqual(1, result.acceleration.timestamp)
        self.assertEqual(2, result.angular_velocity.timestamp)
        self.assertEqual(3, result.magnetic_field.timestamp)
        self.assertEqual(4, result.temperature.timestamp)
        self.assertEqual(123, int(result.status))

    def test_can_scale(self):
        data = self.build_value()
        acceleration = Data(Vector([2, 2, 2]), 11)
        angular_velocity = Data(Vector([3, 3, 3]), 22)
        magnetic_field = Data(Vector([4, 4, 4]), 33)
        temperature = Data(5, 4)
        data2 = NineDoFData(acceleration, angular_velocity, magnetic_field, temperature)
        result = data.scale(data2)  # type: NineDoFData
        self.assertEqual(6.15, result.temperature.value)
        self.assertEqual(Vector([2, 4, 6]), result.acceleration.value)
        self.assertEqual(Vector([12, 15, 18]), result.angular_velocity.value)
        self.assertEqual(Vector([28, 32, 36]), result.magnetic_field.value)

    def test_result_of_scale_has_timestamps_and_status_from_self(self):
        data = self.build_value()
        data2 = self.build_value()
        result = data.scale(data2)  # type: NineDoFData
        self.assertEqual(1, result.acceleration.timestamp)
        self.assertEqual(2, result.angular_velocity.timestamp)
        self.assertEqual(3, result.magnetic_field.timestamp)
        self.assertEqual(4, result.temperature.timestamp)
        self.assertEqual(123, int(result.status))

    def test_to_json(self):
        data = self.build_value()
        actual = data.to_json()
        self.assertEqual('{\n  "acceleration":{"value":{"x":1, "y":2, "z":3}, "timestamp":1},\n  "angular_velocity":{"value":{"x":4, "y":5, "z":6}, "timestamp":2},\n  "magnetic_field":{"value":{"x":7, "y":8, "z":9}, "timestamp":3},\n  "temperature":{"value":1.23, "timestamp":4},\n  "status":"0x7B"\n}',
                         actual)

    def test_from_json(self):
        obj = loads('{"acceleration":{"value":{"x":1, "y":2, "z":3}, "timestamp":1}, '
                    '"angular_velocity":{"value":{"x":4, "y":5, "z":6}, "timestamp":2}, '
                    '"magnetic_field":{"value":{"x":7, "y":8, "z":9}, "timestamp":3}, '
                    '"temperature":{"value":1.23, "timestamp":4}, "status":"0x7B"}')
        actual = NineDoFData.from_json(obj)
        self.assertEqual(self.build_value(), actual)

    def test_from_json_without_status(self):
        obj = loads('{"acceleration":{"value":{"x":1, "y":2, "z":3}, "timestamp":1}, '
                    '"angular_velocity":{"value":{"x":4, "y":5, "z":6}, "timestamp":2}, '
                    '"magnetic_field":{"value":{"x":7, "y":8, "z":9}, "timestamp":3}, '
                    '"temperature":{"value":1.23, "timestamp":4}}')
        actual = NineDoFData.from_json(obj)
        expected = self.build_value()
        expected.status = Flags(0)
        self.assertEqual(expected, actual)

    @staticmethod
    def build_value() -> NineDoFData:
        acceleration = Data(Vector([1, 2, 3]), 1)
        angular_velocity = Data(Vector([4, 5, 6]), 2)
        magnetic_field = Data(Vector([7, 8, 9]), 3)
        temperature = Data(1.23, 4)
        return NineDoFData(acceleration, angular_velocity, magnetic_field, temperature, Flags(123))
