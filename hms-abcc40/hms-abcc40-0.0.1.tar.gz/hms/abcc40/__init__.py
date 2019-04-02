# Copyright 2019 HMS Industrial Networks AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Interface for accessing Anybus CompactCom 40 modules via REST"""

import json
import urllib2


class CompactCom40(object):
    """Class for accessing Anybus CompactCom 40 module via REST"""

    def __init__(self, Ip):
        """Initialize a CompactCom40 instance.

        Ip shall be the IP address of the Anybus CompactCom 40 being read,
        as a dot separated string."""
        self.Ip = Ip

    def _get(self, path, key):
        """Read json object and return value of the key"""
        return json.loads(
            urllib2.urlopen("http://{}/{}".format(self.Ip, path)).read())[key]

    @property
    def module_name(self):
        """Module name as a string"""
        return self._get("module/info.json", "modulename")

    @property
    def serial_number(self):
        """Serial number as a string"""
        return self._get("module/info.json", "serial")

    @property
    def firmware_version(self):
        """Firmware version as a sequence of (major, minor, build)"""
        return self._get("module/info.json", "fwver")

    @property
    def firmware_version_text(self):
        """Firmware version as a string"""
        return self._get("module/info.json", "fwvertext")

    @property
    def uptime(self):
        """Uptime as a number"""
        high, low = self._get("module/info.json", "uptime")
        return (high << 32) + low

    @property
    def cpu_load(self):
        """CPU load as a float (0 - 1)"""
        return self._get("module/info.json", "cpuload") / 100.0

    @property
    def vendor_name(self):
        """Vendor name as a string"""
        return self._get("module/info.json", "vendorname")

    @property
    def hardware_version_text(self):
        """Hardware version as a string"""
        return self._get("module/info.json", "hwvertext")

    @property
    def network_type(self):
        """Network type as a string"""
        return self._get("module/info.json", "networktype")
