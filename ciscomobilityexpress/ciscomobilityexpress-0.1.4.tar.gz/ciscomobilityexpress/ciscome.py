# -*- coding: utf-8 -*-

"""
Support for Cisco Mobility Express.
"""

import requests
import logging

from collections import namedtuple
from .exceptions import CiscoMEConfigError, \
    CiscoMELoginError, CiscoMEPageNotFoundError
from .constants import Constants

log = logging.getLogger(__name__)


class CiscoMobilityExpress:

    def __init__(self, host,
                 username='cisco',
                 password='cisco',
                 is_https=False,
                 verify_ssl=True):
        if not host:
            raise CiscoMEConfigError('host cannot be empty. '
                                     'Use the IP or hostname of your'
                                     'Cisco Mobility Express controller')

        protocol = 'http' if not is_https else 'https'
        self.host = host
        self.host_api_url = '{}://{}'.format(protocol, host)
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.logged_in = False
        self.get_system_info()

    def get_system_info(self):
        """Retrieve system info from Cisco ME."""
        url = Constants.SYSTEM_INFO_URL.format(self.host_api_url)
        json_data = self._call_api(url)
        log.info("version: %s", json_data['version'])
        self.logged_in = True

    def is_logged_in(self):
        """Returns true if a successful login has happened"""
        return self.logged_in

    def get_associated_devices(self):
        """Retrieve data from Cisco ME and return a list of tuples."""
        results_list = []
        table_url = Constants.CLIENT_TABLE_URL.format(self.host_api_url)
        dhcp_url = Constants.CLIENTS_URL.format(self.host_api_url)
        client_table_data = self._call_api(table_url)
        dhcp_data = self._call_api(dhcp_url)

        for device_entry in client_table_data['data']:
            device_entry['controller'] = self.host

            # find the hostname for the entry (clId)
            for dhcp_entry in dhcp_data['data']:
                if dhcp_entry['macaddr'] == device_entry['macaddr']:
                    if 'clId' in dhcp_entry:
                        device_entry['clId'] = dhcp_entry['clId']

            device = namedtuple("Device", device_entry.keys())(
                *device_entry.values())
            results_list.append(device)

        log.debug(results_list)
        return results_list

    def _call_api(self, url):
        """Perform one api request operation."""

        log.info("_call_api : %s" % url)
        response = self.session.get(
            url, auth=(self.username, self.password),
            verify=self.verify_ssl)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 401:
            raise CiscoMELoginError("Failed to authenticate "
                                    "with Cisco Mobility Express "
                                    "controller, check your "
                                    "username and password.")
        elif response.status_code == 404:
            raise CiscoMEPageNotFoundError("Cisco Mobility Express responded "
                                           "with a 404 "
                                           "from %s", url)

        log.error("Invalid response from "
                  "Cisco Mobility Express: %s", response)
        return []
