import unittest

from decawave_1001_rjg import TlvMessage, DwmPosition

from rover_position_rjg.sensors.decawave.csv.dwm_position_to_csv import DwmPositionCsvConverter


class TestDwmPositionCsvConverter(unittest.TestCase):
    message = TlvMessage(bytes([0x40, 0x01, 0x00, 0x41, 0x0D,
                          0x79, 0x00, 0x00, 0x00,
                          0x32, 0x00, 0x00, 0x00,
                          0xfb, 0x00, 0x00, 0x00,
                          0x64]))

    def setUp(self):
        self.converter = DwmPositionCsvConverter()
        self.position = DwmPosition(self.message, 5)

    def test_to_csv(self):
        csv = self.converter.to_row(self.position)
        expected = [121, 50, 251, 100]
        self.assertEqual(expected, csv)

    def test_to_object(self):
        obj = self.converter.to_object([121, 50, 251, 100])
        expected = bytes([0x79, 0x00, 0x00, 0x00,
                          0x32, 0x00, 0x00, 0x00,
                          0xfb, 0x00, 0x00, 0x00,
                          0x64])
        self.assertEqual(expected, obj.message.message)

    def test_to_object_from_strings(self):
        obj = self.converter.to_object(['121', '50', '251', '100'])
        expected = bytes([0x79, 0x00, 0x00, 0x00,
                          0x32, 0x00, 0x00, 0x00,
                          0xfb, 0x00, 0x00, 0x00,
                          0x64])
        self.assertEqual(expected, obj.message.message)
