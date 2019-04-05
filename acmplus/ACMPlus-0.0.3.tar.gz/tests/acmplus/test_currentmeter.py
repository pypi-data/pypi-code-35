import unittest

from acmplus.acmplus import ACMPlusDaemon
from buoy.tests.base_device_tests import BaseDeviceTest


class TestDeviceCurrentMeter(BaseDeviceTest):
    device_class = ACMPlusDaemon
    DEVICE_NAME = 'acmplus'
    config_buoy_file = "tests/support/config/acmplus.yaml"
    __test__ = True


if __name__ == '__main__':
    unittest.main()
