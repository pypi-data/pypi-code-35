import unittest
from json import loads

from rover_position_rjg.data.data import *
from rover_position_rjg.data.vector import Vector


class DataTest(unittest.TestCase):

    def test_initialises_properties(self):
        data = Data("value", 123)
        self.assertEqual(data.value, 'value')
        self.assertEqual(data.timestamp, 123)

    def test_equal(self):
        data1 = Data("value", 123)
        self.assertEqual(data1, data1)
        data2 = Data("value", 123)
        self.assertEqual(data1, data2)
        self.assertFalse(data1 == 'fish')
        different = Data("diff", 123)
        self.assertFalse(data1 == different)
        different = Data("value", 5)
        self.assertFalse(data1 == different)

    def test_not_equal(self):
        data1 = Data("value", 123)
        self.assertFalse(data1 != data1)
        data2 = Data("value", 123)
        self.assertFalse(data1 != data2)
        self.assertTrue(data1 != 'fish')
        different = Data("diff", 123)
        self.assertTrue(data1 != different)
        different = Data("value", 5)
        self.assertTrue(data1 != different)

    def test_repr(self):
        data1 = Data("value", 123)
        self.assertEqual('Data(value, 123)', data1.__repr__())

    def test_to_json_simple_value(self):
        data1 = Data('Fish', 123)
        actual = data1.to_json()
        self.assertEqual('{"value":"Fish", "timestamp":123}', actual)

    def test_to_json_complex_value(self):
        data1 = Data(Vector.one(), 123)
        actual = data1.to_json()
        self.assertEqual('{"value":{"x":1, "y":1, "z":1}, "timestamp":123}', actual)

    def test_from_json_simple_value(self):
        obj = loads('{"value":"Fish", "timestamp":123}')
        actual = Data.from_json(obj)
        self.assertEqual(Data('Fish', 123), actual)

    def test_from_json_complex_value(self):
        obj = loads('{"value":{"x":1, "y":1, "z":1}, "timestamp":123}')
        actual = Data[Vector].from_json(obj, Vector.from_json)
        self.assertEqual(Data(Vector.one(), 123), actual)


if __name__ == '__main__':
    unittest.main()
