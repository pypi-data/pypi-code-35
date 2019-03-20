from typing import Any, Callable

from rover_position_rjg.data.data_filter import DataFilter
from rover_position_rjg.mqtt.mqtt_client import MqttClient
from rover_position_rjg.services.message_helpers.filter_toggle import FilterToggle


class MqttFilterToggle(FilterToggle):
    """Like filter toggle except that it attaches start and stop to message callbacks"""
    _filter: DataFilter[Any, Any]

    def __init__(self,
                 mqtt_client: MqttClient,
                 root_filter: DataFilter,
                 attachment_filter_name: str,
                 stop_topic: str,
                 start_topic: str,
                 start_callback:  Callable[[str], DataFilter[Any, Any]],
                 stop_callback: Callable[[None], None] = None):
        super().__init__(root_filter, attachment_filter_name, start_callback, stop_callback)
        self._mqtt_client = mqtt_client
        self._mqtt_client.on(stop_topic, self.stop)
        self._mqtt_client.on_message(start_topic, self.start)

