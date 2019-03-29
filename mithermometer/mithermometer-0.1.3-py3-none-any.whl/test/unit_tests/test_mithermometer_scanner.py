"""Test the mithermometer_scanner."""

import unittest
from mithermometer import mithermometer_scanner


class TestMithermometerScanner(unittest.TestCase):
    """Test the miflora_scanner."""

    def test_scan(self):
        """Test the scan function."""

        class _MockBackend:  # pylint: disable=too-few-public-methods
            """Mock of the backend, always returning the same devices."""

            @staticmethod
            def scan_for_devices(_):
                """Mock for the scan function."""
                return [
                    ('00:FF:FF:FF:FF:FF', None),
                    ('01:FF:FF:FF:FF:FF', 'MJ_HT_V1'),
                    ('4C:65:A8:FF:FF:FF', 'random name'),
                ]

        devices = mithermometer_scanner.scan(_MockBackend, 0)
        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0], '01:FF:FF:FF:FF:FF')
        self.assertEqual(devices[1], '4C:65:A8:FF:FF:FF')
