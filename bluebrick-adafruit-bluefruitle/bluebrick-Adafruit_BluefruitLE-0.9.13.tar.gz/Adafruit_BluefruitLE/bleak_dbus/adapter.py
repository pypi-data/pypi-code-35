# Python object to represent the bluez DBus adapter object.  Provides properties
# and functions to easily interact with the DBus object.
# Author: Tony DiCola
#
# Copyright (c) 2015 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from ..config import TIMEOUT_SEC
from ..interfaces import Adapter
import asyncio




class BleakAdapter(Adapter):
    """Bleak BLE network adapter."""

    def __init__(self, dbus_obj):
        """Create an instance of the bluetooth adapter from the provided bluez
        DBus object.
        """
        self._is_scanning = False
        self._is_power_on = False
        # Create the run loop here
        self.loop = asyncio.get_event_loop()

    @property
    def name(self):
        """Return the name of this BLE network adapter."""
        return "Default adapter"

    def start_scan(self, timeout_sec=TIMEOUT_SEC):
        """Start scanning for BLE devices with this adapter."""
        # Don't do anything
        self._is_scanning = True
        return


    def stop_scan(self, timeout_sec=TIMEOUT_SEC):
        """Stop scanning for BLE devices with this adapter."""
        return
        self._is_scanning = False

    @property
    def is_scanning(self):
        """Return True if the BLE adapter is scanning for devices, otherwise
        return False.
        """
        return self._is_scanning

    def power_on(self):
        """Power on this BLE adapter."""
        self._is_power_on = True
        return 

    def power_off(self):
        """Power off this BLE adapter."""
        self._is_power_on = False
        return

    @property
    def is_powered(self):
        """Return True if the BLE adapter is powered up, otherwise return False.
        """
        return self.is_power_on
