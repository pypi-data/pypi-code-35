import jsonpickle

from rover_position_rjg.data.data import TValue, Data
from rover_position_rjg.data.data_filter import DataFilter
from rover_position_rjg.mqtt.mqtt_client import MqttClient


class PublishFilter(DataFilter[TValue, TValue]):
    """Publishes a message to an MQTT topic."""

    def __init__(self, topic: str, mqtt_client: MqttClient):
        super().__init__()
        self.topic = topic
        self.mqtt_client = mqtt_client

    def receive(self, data: Data[TValue]) -> None:
        payload = jsonpickle.encode(data)
        self.mqtt_client.publish(self.topic, payload)
        self.send(data)

    def close(self):
        # Nothing to do
        pass
