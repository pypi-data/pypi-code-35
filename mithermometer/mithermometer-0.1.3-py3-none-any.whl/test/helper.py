"""Helper functions for unit tests."""
from test import HANDLE_READ_NAME, HANDLE_READ_SENSOR_DATA, HANDLE_READ_VERSION, HANDLE_READ_BATTERY

from btlewrap.base import AbstractBackend, BluetoothBackendException


class MockBackend(AbstractBackend):
    """Mockup of a Backend and Sensor.

    The behaviour of this Sensors is based on the knowledge there
    is so far on the behaviour of the sensor. So if our knowledge
    is wrong, so is the behaviour of this sensor! Thus is always
    makes sensor to also test against a real sensor.
    """

    def __init__(self, adapter='hci0'):
        super(MockBackend, self).__init__(adapter)
        self._version = (0, 0, 0)
        self.name = ''
        self.battery_level = 0
        self.temperature = None
        self.humidity = None
        self.expected_write_handles = set()
        self.override_read_handles = dict()
        self.is_available = True
        self._handle_0x35_raw_set = False
        self._handle_0x35_raw = None
        self._handle_0x03_raw_set = False
        self._handle_0x03_raw = None
        self._handle_0x38_raw_set = False
        self._handle_0x38_raw = None

    def check_backend(self):
        """This backend is available when the field is set accordingly."""
        return self.is_available

    def set_version(self, major, minor, patch):
        """Sets the version number to be returned."""
        self._version = (major, minor, patch)

    @property
    def version(self):
        """Get the stored version number as string."""
        return '{}.{}.{}'.format(*self._version)

    def read_handle(self, handle):
        """Read one of the handles that are implemented."""
        if handle in self.override_read_handles:
            return self.override_read_handles[handle]
        if handle == HANDLE_READ_VERSION:
            return self._read_version()
        if handle == HANDLE_READ_BATTERY:
            return self._read_battery()
        if handle == HANDLE_READ_SENSOR_DATA:
            return self._read_sensor_data()
        if handle == HANDLE_READ_NAME:
            return self._read_name()

        raise ValueError('handle not implemented in mockup')

    def wait_for_notification(self, handle, delegate, notification_timeout):  # pylint: disable=unused-variable
        if self.temperature is not None and self.humidity is not None:
            delegate.handleNotification(None, bytes("T={:.1f} H={:.1f} ".format(self.temperature, self.humidity),
                                                    'utf-8'))
        else:
            delegate.handleNotification(None, None)
        return True

    def _read_battery(self):
        """Recreate the battery level string from the fields of this class."""
        if self._handle_0x38_raw_set:
            return self._handle_0x38_raw
        result = [self.battery_level, 0xFF]
        return bytes(result)

    def _read_version(self):
        return bytes(self.version, 'utf-8')

    def _read_sensor_data(self):
        """Recreate sensor data from the fields of this class."""
        if self._handle_0x35_raw_set:
            return self._handle_0x35_raw

        class Cache:  # pylint: disable=missing-docstring,too-few-public-methods
            value = None

            @staticmethod
            def handleNotification(_, data):  # pylint: disable=invalid-name
                Cache.value = data

        self.wait_for_notification(None, Cache.value, None)

        return bytes(Cache.value)

    def _read_name(self):
        """Convert the name into a byte array and return it."""
        if self._handle_0x03_raw_set:
            return self._handle_0x03_raw
        return [ord(c) for c in self.name]

    @property
    def handle_0x35_raw(self):
        """Getter for handle_0x35_raw."""
        return self._handle_0x35_raw

    @handle_0x35_raw.setter
    def handle_0x35_raw(self, value):
        """Setter for handle_0x35_raw.

        This needs a separate flag so that we can also use "None" as return value.
        """
        self._handle_0x35_raw_set = True
        self._handle_0x35_raw = value

    @property
    def handle_0x03_raw(self):
        """Getter for handle_0x03_raw."""
        return self._handle_0x03_raw

    @handle_0x03_raw.setter
    def handle_0x03_raw(self, value):
        """Setter for handle_0x33_raw.

        This needs a separate flag so that we can also use "None" as return value.
        """
        self._handle_0x03_raw_set = True
        self._handle_0x03_raw = value

    @property
    def handle_0x38_raw(self):
        """Getter for handle_0x38_raw."""
        return self._handle_0x38_raw

    @handle_0x38_raw.setter
    def handle_0x38_raw(self, value):
        """Setter for handle_0x33_raw.

        This needs a separate flag so that we can also use "None" as return value.
        """
        self._handle_0x38_raw_set = True
        self._handle_0x38_raw = value


class ConnectExceptionBackend(AbstractBackend):
    """This backend always raises Exceptions."""

    def connect(self, mac):
        """Raise exception when connecting."""
        raise BluetoothBackendException('always raising exceptions')

    def disconnect(self):
        """Disconnect always works"""

    def check_backend(self):
        """check backend must pass so that we get to the BT communication."""
        return True


class RWExceptionBackend(AbstractBackend):
    """This backend always raises Exceptions."""

    def connect(self, mac):
        """Connect always works"""

    def disconnect(self):
        """Disconnect always works"""

    def check_backend(self):
        """check backend must pass so that we get to the BT communication."""
        return True

    def read_handle(self, _):
        """Reading always fails."""
        raise BluetoothBackendException('always raising')

    def read_write(self, _, __):  # pylint: disable=no-self-use
        """Writing always fails."""
        raise BluetoothBackendException('always raising')
