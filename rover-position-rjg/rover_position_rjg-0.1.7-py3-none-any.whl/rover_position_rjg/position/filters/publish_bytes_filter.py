from rover_position_rjg.data.data import Data
from rover_position_rjg.data.data_filter import DataFilter
from rover_position_rjg.mqtt.mqtt_client import MqttClient


class PublishBytesFilter(DataFilter[bytes, bytes]):
    """Publishes bytes to an MQTT topic."""

    def __init__(self, topic: str, mqtt_client: MqttClient):
        super().__init__()
        self.topic = topic
        self.mqtt_client = mqtt_client

    def receive(self, data: Data[bytes]) -> None:
        self.mqtt_client.publish(self.topic, data.value)
        self.send(data)

    def close(self):
        # Nothing to do
        pass
