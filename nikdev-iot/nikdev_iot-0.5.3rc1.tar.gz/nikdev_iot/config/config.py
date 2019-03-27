# -*- coding: utf-8 -*-


class Config:
    """
    Configuration class that stores values for the API.
    """

    _config_custom = {}
    """
    Dict with custom configuration values, overrides the _config_default values.
    """

    _config_default = {
        "baseUrl": "https://iot.nik-dev.se/api/v1/",
        "deviceId": None,
        "apiKey": None,
        "storagePath": "",
        "storageFilename": "iot_storage.db",
        "stageUncommittedValues": True,
        "stageUnpushedEntries": True,

        "requestTimeout": 10,
    }
    """
    Dict with default configuration values.
    """

    def __init__(self, config=None):
        # If the custom path is set, read it
        if config is not None:
            self._config_custom = config
        else:
            self._config_custom = {}

    def has_value(self, key):
        """
        Checks whether the key exists in the current configuration scope.

        :param key:     The key to look after (needle).
        :type key: str
        :return:        True if the key was found, otherwise false.
        """
        return key in self._config_custom or \
               key in self._config_default

    def get_value(self, key, default=None):
        """
        Gets a value from the custom or default configuration (with priority to custom config).

        :param key:     The key to set the value from.
        :type key: str
        :param default: If no value was found, return default value instead.
        :return:        The value stored under the key.
        """
        if key in self._config_custom:
            return self._config_custom[key]
        elif key in self._config_default:
            return self._config_default[key]
        else:
            return default

    def set_value(self, key, value):
        """
        Sets a custom value to the current config file.

        :param key:     The key to set the value as.
        :type key: str
        :param value:   The value to store under the key.
        """
        self._config_custom[key] = value

