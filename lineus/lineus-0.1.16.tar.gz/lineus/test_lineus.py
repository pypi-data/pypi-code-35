import unittest
import lineus


class TestConnect(unittest.TestCase):

    def test_successful_connect(self):
        my_line_us = lineus.LineUs()
        success = my_line_us.connect('line-us.local')
        my_line_us.disconnect()
        self.assertTrue(success)

    def test_successful_connect_default_name(self):
        my_line_us = lineus.LineUs()
        success = my_line_us.connect(wait=5)
        my_line_us.disconnect()
        self.assertTrue(success)

    def test_unsuccessful_connect(self):
        my_line_us = lineus.LineUs()
        success = my_line_us.connect('wgrhmftmf.local')
        my_line_us.disconnect()
        self.assertFalse(success)


if __name__ =='__main__':
    unittest.main()
