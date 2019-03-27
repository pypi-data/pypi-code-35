# -*- coding: utf-8 -*-

import atexit
import os
import time
import shelve

from nikdev_iot.config import Config
from nikdev_iot.network.network import NetworkStatus
from nikdev_iot.objects import Value, Entry, Batch
from nikdev_iot.network import Network
from nikdev_iot.serializers import ValueSerializer

from .exceptions import PushException, GetException


class _BaseApi(object):

    config = None
    """
    The configuration class for the API. Can be used to access configuration values.
    
    :type: Config
    """

    network = None

    def __init__(self, config=None):
        """
        Initializes the API with a config dictionary.

        :param config:      The given API key needed to connect to the server.
        :type config: dict
        """
        # Store the config locally
        self.config = Config(config)
        self.network = Network(self.config)

    @classmethod
    def from_credentials(cls, device_id, api_key):
        """
        Initializes the API with credentials only and uses the default settings for everything else.

        :param device_id:   The id of the device that the API is trying to connect to.
        :param api_key:     The given API key needed to connect to the server.
        :type device_id: str
        :type api_key: str
        """
        return cls({
            'deviceId': device_id,
            'apiKey': api_key
        })


class _UpstreamApi(_BaseApi):

    values = []  # type: List[Any]
    """
    Stores added values that hasn't been committed yet.
    
    :type: list[Value]
    """

    entries = []
    """
    Stores committed entries that hasn't been pushed yet.
    
    :type: list[object]
    """

    def add_value(self, field_id, value):
        """
        Adds a value to be committed and updates it if a value with the field_id already exists.

        :param field_id:    The represented field_id
        :param value:       The value to store.
        :return:            Returns the added Value object.
        :rtype: Value
        """
        # Sets initial variable to check if the value was updated or not
        updated = False
        # Create the value object
        new_value_object = Value(field_id, value)
        # Iterate over all added values
        for idx, old_value_object in enumerate(self.values):
            # Check if the new value has already been set previously.
            if old_value_object == new_value_object:
                # If so, update it instead.
                self.values[idx] = new_value_object
                updated = True

        # Check if we updated the value or not
        if not updated:
            # If we didn't add it to values instead.
            self.values.append(new_value_object)

        return new_value_object

    def commit(self):
        """
        Stores the added values to an entry that can be sent to the server.
        This step must be done before pushing.
        """
        # Get the current timestamp
        commit_timestamp = int(time.time())
        # Create a new entry, and pass the values by value (instead of by reference)
        entry = Entry(timestamp=commit_timestamp, values=self.values[:])
        # Add the entry to the entries
        self.entries.append(entry)
        # Delete the committed values
        self.reset()

    def push(self):
        """
        Takes the committed entries and send them to the server.

        :rtype: None
        """
        client_timestamp = int(time.time())
        batch = Batch(timestamp=client_timestamp, entries=self.entries)

        status, response = self.network.post(
            url=self.config.get_value('baseUrl') + 'entries/',
            json=batch.to_object_upstream()
        )

        if status == NetworkStatus.SUCCESS:
            self.reset_unpushed_entries()
        elif status == NetworkStatus.BAD_REQUEST:
            # self.reset_unpushed_entries()
            try:
                error_message = response.json()['message']
            except ValueError:
                error_message = str(response.status_code)
            raise PushException('Bad request: ' + error_message, True)
        elif status == NetworkStatus.BAD_LUCK:
            raise PushException('Bad luck: client timeout or unexpected server error.', True)

    def commit_and_push(self):
        """
        Merged function of commit and push.

        :rtype: None
        """
        self.commit()
        self.push()

    def reset(self):
        """
        Deletes all uncommitted values.
        """
        self.values = []

    def reset_unpushed_entries(self):
        """
        Deletes all entries that haven't been pushed.
        """
        self.entries = []


class _DownstreamApi(_UpstreamApi):

    def get(self, field_ids=None):
        # Make sure the field ids are a list
        if not type(field_ids) == list:
            field_ids = [field_ids]

        # Merge the field ids into a string with commas
        value_str = ','.join(field_ids)

        status, response = self.network.get(
            url=self.config.get_value('baseUrl') + 'values/' + value_str,
        )

        if status == NetworkStatus.SUCCESS:
            return ValueSerializer.serialize_from_server(response.json()['data'])
        elif status == NetworkStatus.BAD_REQUEST:
            try:
                error_message = response.json()['message']
            except ValueError:
                error_message = str(response.status_code)
            raise GetException('Bad request: ' + error_message)
        elif status == NetworkStatus.BAD_LUCK:
            raise GetException('Bad luck: client timeout or unexpected server error.')


class _StorageApi(_DownstreamApi):

    __STORAGE_VERSION = "1.0.0"
    """
    The version of the storage handler. May differ between API versions, but not necessarily.
    Is only used to handle migrations.
    
    :type: str
    """

    storage = shelve
    """
    The storage wrapper that keeps uncommitted data.
    
    :type: shelve.DbfilenameShelf
    """

    def __init__(self, config=None):
        super(_StorageApi, self).__init__(config)

        # Check if any staging functionality is used
        if self.config.get_value('stageUncommittedValues', False) or \
                self.config.get_value('stageUnpushedEntries', False):
            # If so, initialise the storage
            self.storage = self.get_storage()

        # Check if value staging is used
        if self.config.get_value('stageUncommittedValues', False):
            # Restore previously staged values
            self._restore_values()
            # Register destructor, to make sure uncommitted values won't be lost
            atexit.register(self.stage_values)

        # Check if entry staging is used
        if self.config.get_value('stageUnpushedEntries', False):
            # Restore previously staged entries
            self._restore_entries()
            # Register destructor, to make sure unpushed entries won't be lost
            atexit.register(self.stage_entries)

    def get_storage(self):
        """
        Initialises and returns the storage handler used for the API.
        The storage is used to stage uncommitted values and unpushed
        entries in case of an exception or failure.

        :return: A storage object used for the API.
        :rtype: shelve.DbfilenameShelf
        """
        # Get the path to the storage
        path = self.config.get_value('storagePath', "")
        # Get the name of the file
        name = self.config.get_value('storageName', "iot_storage.db")
        # Bind the path and name together properly
        storage = shelve.open(os.path.join(path, name))

        # Check if there's a previous storage or if it's brand new.
        if not storage.has_key("version") or storage.get("version", "") == "":
            # The storage is new, we need to set up some things
            # Set the version to the current so it won't initialise on next run
            storage['version'] = self.__STORAGE_VERSION
            # Set the value and entry lists empty
            storage['values'] = []
            storage['entries'] = []

        return storage

    def stage_values(self):
        new_values = []
        for val in self.values:  # type: Value
            new_values.append(val.to_object_storage())
        self.storage['values'] = new_values
        self.values = []

    def stage_entries(self):
        new_entries = []
        for entry in self.entries:  # type: Entry
            new_entries.append(entry.to_object_storage())
        self.storage['entries'] = new_entries
        self.entries = []

    def _restore_values(self):
        for val in self.storage.get('values', []):
            self.values.append(Value.from_json_storage(val))
        self.storage['values'] = []

    def _restore_entries(self):
        for val in self.storage.get('entries', []):
            self.entries.append(Entry.from_json_storage(val))
        self.storage['entries'] = []


# class Api(_StorageApi):  # Bypass the storage api for now since no function is ready.
class Api(_StorageApi):
    """
    Endpoint and wrapper for sending and receiving data from the NikDev IoT Server.
    """
    pass
