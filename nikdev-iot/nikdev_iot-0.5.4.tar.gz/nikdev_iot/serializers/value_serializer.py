# -*- coding: utf-8 -*-

from nikdev_iot.objects import Value
import time


class ValueSerializer:

    def __init__(self):
        pass

    @staticmethod
    def serialize_from_server(json_data):
        """
        Takes a server response for getting values and transforms it into a list of Values with adjusted timestamps.

        :type json_data: dict
        """
        # Extract the values from the data
        values_json = json_data.get('values')

        # Get the local timestamp
        local_timestamp = time.time()
        # Get hte server timestamp
        server_timestamp = int(json_data.get('servertime'))

        # Get the offset between the local time and server time
        offset = int(round(local_timestamp - server_timestamp))

        values = []
        # Iterate over each value
        for value_json in values_json:
            # Get the value from serializing it
            value = Value.from_json_downstream(value_json)
            # Adjust the timestamp with the offset
            value.adjust_timestamp(offset)
            values.append(value)

        return values
