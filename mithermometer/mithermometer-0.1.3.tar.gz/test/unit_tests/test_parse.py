""" Test parsing of binary data.

Created on Aug 8, 2018

@author: hobbypunk
"""

import unittest
from datetime import datetime
from test.helper import MockBackend
from mithermometer.mithermometer_poller import MiThermometerPoller, \
    MI_TEMPERATURE, MI_HUMIDITY


class KNXConversionTest(unittest.TestCase):
    """Test parsing of binary data."""
    # in testing access to protected fields is OK
    # pylint: disable=protected-access

    def test_parsing(self):
        """Does the Mi Thermometer data parser works correctly?"""
        poller = MiThermometerPoller(None, MockBackend)
        data = bytes('T=29.3 H=40.3 ', 'utf-8')
        poller._cache = data
        poller._last_read = datetime.now()
        self.assertEqual(poller._parse_data()[MI_TEMPERATURE], 29.3)
        self.assertEqual(poller._parse_data()[MI_HUMIDITY], 40.3)

        data = bytes('T=24.2 H=45.3 ', 'utf-8')
        poller._cache = data
        poller._last_read = datetime.now()
        self.assertEqual(poller._parse_data()[MI_TEMPERATURE], 24.2)
        self.assertEqual(poller._parse_data()[MI_HUMIDITY], 45.3)
