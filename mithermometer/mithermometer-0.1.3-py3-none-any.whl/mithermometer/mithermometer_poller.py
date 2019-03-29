""""
Read data from Mi thermometer sensor.
"""

import re

from datetime import datetime, timedelta
import logging
from threading import Lock
from btlewrap.base import BluetoothInterface, BluetoothBackendException

_HANDLE_READ_NAME = 0x03
_HANDLE_READ_BATTERY = 0x18
_HANDLE_READ_VERSION = 0x24
_HANDLE_READ_SENSOR_DATA = 0x10

MI_TEMPERATURE = "temperature"
MI_HUMIDITY = "humidity"
MI_BATTERY = "battery"

_LOGGER = logging.getLogger(__name__)


class MiThermometerPoller:
    """"
    A class to read data from Mi thermometer sensors.
    """

    def __init__(self, mac, backend, cache_timeout=600, retries=3, adapter='hci0'):
        """
        Initialize a Mi Thermometer Poller for the given MAC address.
        """

        self._mac = mac
        self._bt_interface = BluetoothInterface(backend, adapter)
        self._cache = None
        self._cache_timeout = timedelta(seconds=cache_timeout)
        self._last_read = None
        self._fw_last_read = None
        self._batt_last_read = None
        self.retries = retries
        self.ble_timeout = 10
        self.lock = Lock()
        self._firmware_version = None
        self.battery = None

    def name(self):
        """Return the name of the sensor."""
        with self._bt_interface.connect(self._mac) as connection:
            name = connection.read_handle(_HANDLE_READ_NAME)  # pylint: disable=no-member

        if not name:
            raise BluetoothBackendException("Could not read data from Mi Flora sensor %s" % self._mac)
        return ''.join(chr(n) for n in name)

    def fill_cache(self):
        """Fill the cache with new data from the sensor."""
        _LOGGER.debug('Filling cache with new sensor data.')
        try:
            self.firmware_version()
        except BluetoothBackendException:
            # If a sensor doesn't work, wait 5 minutes before retrying
            self._last_read = datetime.now() - self._cache_timeout + \
                timedelta(seconds=300)
            raise

        with self._bt_interface.connect(self._mac) as connection:
            class Cache: # pylint: disable=too-few-public-methods
                """
                Cache class for wait for notification callback
                """
                value = None
                @staticmethod
                def handleNotification(_, data):  # pylint: disable=invalid-name,missing-docstring
                    Cache.value = data

            # pylint: disable=no-member
            connection.wait_for_notification(_HANDLE_READ_SENSOR_DATA, Cache, self.ble_timeout)
            _LOGGER.debug('Received result for handle %s: %s',
                          _HANDLE_READ_SENSOR_DATA, self._format_bytes(Cache.value))
            self._cache = Cache.value
            self._check_data()
            if self.cache_available():
                self._last_read = datetime.now()
            else:
                # If a sensor doesn't work, wait 5 minutes before retrying
                self._last_read = datetime.now() - self._cache_timeout + \
                    timedelta(seconds=300)

    def battery_level(self):
        """Return the battery level."""
        if (self.battery is None) or \
                (datetime.now() - timedelta(hours=1) > self._batt_last_read):
            self._batt_last_read = datetime.now()
            with self._bt_interface.connect(self._mac) as connection:
                res = connection.read_handle(_HANDLE_READ_BATTERY)  # pylint: disable=no-member
                _LOGGER.debug('Received result for handle %s: %s',
                              _HANDLE_READ_BATTERY, self._format_bytes(res))
            if res is None:
                self.battery = 0
            else:
                self.battery = res[0]
        return self.battery

    def firmware_version(self):
        """Return the firmware version."""
        if (self._firmware_version is None) or (datetime.now() - timedelta(hours=24) > self._fw_last_read):
            self._fw_last_read = datetime.now()
            with self._bt_interface.connect(self._mac) as connection:
                res = connection.read_handle(_HANDLE_READ_VERSION)  # pylint: disable=no-member
                _LOGGER.debug('Received result for handle %s: %s',
                              _HANDLE_READ_VERSION, self._format_bytes(res))
            if res is None:
                self._firmware_version = None
            else:
                self._firmware_version = "".join(map(chr, res))
        return self._firmware_version

    def parameter_value(self, parameter, read_cached=True):
        """Return a value of one of the monitored paramaters.

        This method will try to retrieve the data from cache and only
        request it by bluetooth if no cached value is stored or the cache is
        expired.
        This behaviour can be overwritten by the "read_cached" parameter.
        """
        # Special handling for battery attribute
        if parameter == MI_BATTERY:
            return self.battery_level()

        # Use the lock to make sure the cache isn't updated multiple times
        with self.lock:
            if (read_cached is False) or \
                    (self._last_read is None) or \
                    (datetime.now() - self._cache_timeout > self._last_read):
                self.fill_cache()
            else:
                _LOGGER.debug("Using cache (%s < %s)",
                              datetime.now() - self._last_read,
                              self._cache_timeout)

        if self.cache_available() and (len(self._cache) >= 12) and (len(self._cache) <= 14):
            return self._parse_data()[parameter]
        raise BluetoothBackendException("Could not read data from Mi Flora sensor %s" % self._mac)

    def _check_data(self):
        """Ensure that the data in the cache is valid.

        If it's invalid, the cache is wiped.
        """
        if not self.cache_available():
            return
        if sum(self._cache) == 0:
            self.clear_cache()
            return

    def clear_cache(self):
        """Manually force the cache to be cleared."""
        self._cache = None
        self._last_read = None

    def cache_available(self):
        """Check if there is data in the cache."""
        return self._cache is not None

    def _parse_data(self):
        """Parses the byte array returned by the sensor.

        The sensor returns a string with 14 bytes. Example: "T=26.2 H=45.4\x00"
        """
        data = self._cache
        res = dict()
        res[MI_TEMPERATURE], res[MI_HUMIDITY] = re.sub("[TH]=", '', data[:-1].decode()).split(' ')
        res[MI_TEMPERATURE] = float(res[MI_TEMPERATURE])
        res[MI_HUMIDITY] = float(res[MI_HUMIDITY])
        return res

    @staticmethod
    def _format_bytes(raw_data):
        """Prettyprint a byte array."""
        if raw_data is None:
            return 'None'
        return ' '.join([format(c, "02x") for c in raw_data]).upper()
