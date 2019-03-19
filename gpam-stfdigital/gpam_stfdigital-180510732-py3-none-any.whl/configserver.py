"""
Module for generate config dict from configserver
"""

import os
import requests
from logger import logger

class ConfigServer:
    """Encapsulate config dict avoiding
       developers to modify this content"""

    CONFIG_HOST = '{}{}/{}{}.json'

    def __init__(self):

        logger.debug('Requesting configuration file')

        config_address = os.environ['CONFIGSERVER_ADDRESS']
        branch = '/' + os.environ['CONFIGSERVER_BRANCH']
        app_name = os.environ['APP_NAME']
        profile = '-' + os.environ['PROFILES']

        if branch == '/':
            branch = ''

        config_host = os.path.join(self.CONFIG_HOST.format(config_address, branch, app_name, profile))

        logger.debug(f'Config host url: {config_host}')
        response = requests.get(config_host)
        self._config_content = response.json()

        logger.debug(f'Config content: {self._config_content}')
        logger.debug('Config file taked')

    def get_atribute(self, key_attr):
        """
        Get a atribute from configuration file
        use . to define a path on a key tree
        """

        key_list = key_attr.split('.')
        atribute_content = self._config_content.get(key_list[0])

        for key in key_list[1:]:
            atribute_content = atribute_content.get(key)
            
        logger.debug('Getting atribute from content')

        return atribute_content

    def get_keys(self):
        """
        List all keys from config file
        """

        keys = self._config_content.keys()

        logger.debug('Gettings keys from config file')

        return keys
