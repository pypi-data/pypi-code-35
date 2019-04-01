import os
import copy
import unittest

from shelli import transport

class TestTransporter(unittest.TestCase):
    def setUp(self):
        pass

    def test_good_local_file(self):
        t = transport.Transporter('/etc/passwd:/literally/anything')
        # This test passes if nothing gets raised
        self.assertTrue(True)

    def test_bad_local_file(self):
        with self.assertRaises(transport.InvalidTransportFile) as ctx:
            t = transport.Transporter('/not/a/valid/file:/literally/anything')

    def test_bad_tranport_string(self):
        with self.assertRaises(transport.InvalidTransporter) as ctx:
            t = transport.Transporter('/etc/passwd:/any:thing')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
