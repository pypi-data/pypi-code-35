"""
GoodWan client library: event
"""
import datetime

from goodwan_client.classes import Basic
from goodwan_client.devices import Device
from goodwan_client.serializer import DateTimeField, DeviceGenerator, \
    DeviceNameGenerator


class Event(Basic):
    """ Event class """
    id_event = int                      # type: int
    id_system = str                     # type: str
    id_transmitter = int                # type: int
    data_type = int                     # type: int
    data = str                          # type: str
    data_ext = str                      # type: str
    signal_lvl = int                    # type: int
    timestamp = DateTimeField           # type: datetime.datetime
    device = DeviceGenerator            # type: Device
    device_name = DeviceNameGenerator   # type: str
