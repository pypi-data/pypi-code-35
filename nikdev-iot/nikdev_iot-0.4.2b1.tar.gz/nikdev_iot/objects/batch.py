# -*- coding: utf-8 -*-

import time
from . import Entry


class Batch:
    """
    Batch object that contains the current client timestamp and all entries to be sent to the server.
    """

    timestamp = None
    """
    The current timestamp of the server or client (depending if it was retrieved or posted from the server.

    :type: int
    """

    entries = []
    """
    A list of all entries to be sent to the server.
    
    :type: list[Entry]
    """

    def __init__(self, timestamp=None, entries=None):
        """
        Creates an Batch object that can store entries and timestamp of data to be uploaded.

        :param int timestamp:       The timestamp to be set to the server. If empty, set from the current client time.
        :param list[Value] entries: A list of entries to be sent to the server.
        """
        self.timestamp = timestamp if timestamp else int(time.time())
        self.entries = entries if entries else []

    def to_object_downstream(self):
        """
        Converts the object to a dict that looks like the server.

        :return:    A represented dict that matches the structure from the server.
        :rtype:     dict[int, list[Entry]]
        """
        # Serialize all the values before returning the entry.
        serialized_entries = []
        for entry in self.entries:
            serialized_entries.append(entry.to_object_downstream())
        return {
            'serverTimestamp': self.timestamp,
            'entries': serialized_entries
        }

    def to_object_upstream(self):
        """
        Converts the object to a dict that can be sent to the server.

        :return:    A represented dict to store on server.
        :rtype:     dict[int, list[Entry]]
        """
        # Serialize all the values before returning the entry.
        serialized_entries = []
        for entry in self.entries:
            serialized_entries.append(entry.to_object_upstream())
        return {
            'clientTimestamp': self.timestamp,
            'entries': serialized_entries
        }
