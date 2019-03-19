import unittest

from decawave_1001_rjg import TlvMessage, DwmDistanceAndPosition

from rover_position_rjg.sensors.decawave.csv.dwm_distance_and_position_to_csv import DwmDistanceAndPositionCsvConverter


class TestDwmDistanceAndPositionCsvConverter(unittest.TestCase):
    message = TlvMessage(bytes([
        0x49, 0x51, 0x04,
        0xAB, 0xCD,
        0x87, 0x65, 0x43, 0x21,
        0x10,
        0x79, 0x00, 0x00, 0x00, 0x32, 0x00, 0x00, 0x00, 0xfb, 0x00, 0x00, 0x00, 0x64]))

    def setUp(self):
        self.converter = DwmDistanceAndPositionCsvConverter()
        self.dp = DwmDistanceAndPosition(self.message, 3)

    def test_to_csv(self):
        csv = self.converter.to_row(self.dp)
        expected = ['CDAB', 558065031, 16, 121, 50, 251, 100]
        self.assertEqual(expected, csv)

    def test_to_object(self):
        obj = self.converter.to_object(['CDAB', 558065031, 16, 121, 50, 251, 100])
        expected = bytes([0xAB, 0xCD,
                          0x87, 0x65, 0x43, 0x21,
                          0x10,
                          0x79, 0x00, 0x00, 0x00, 0x32, 0x00, 0x00, 0x00, 0xfb, 0x00, 0x00, 0x00, 0x64])
        self.assertEqual(expected, obj.message.message)

    def test_to_object_from_strings(self):
        obj = self.converter.to_object([' \'CDAB\'', '558065031', '16', '121', '50', '251', '100'])
        expected = bytes([0xAB, 0xCD,
                          0x87, 0x65, 0x43, 0x21,
                          0x10,
                          0x79, 0x00, 0x00, 0x00, 0x32, 0x00, 0x00, 0x00, 0xfb, 0x00, 0x00, 0x00, 0x64])
        self.assertEqual(expected, obj.message.message)
