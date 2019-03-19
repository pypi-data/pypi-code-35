from rover_position_rjg.mqtt.mqtt_client import MqttClient


class MessageSwitch:
    def __init__(self, mqtt_client: MqttClient, stop_topic: str, start_topic: str, start_payload: str, already_started: bool = False):
        self._mqtt_client = mqtt_client
        self._stop_topic = stop_topic
        self._start_topic = start_topic
        self._start_payload = start_payload
        self._started = already_started

    def start(self):
        self._mqtt_client.publish(self._start_topic, self._start_payload)
        self._started = True

    def stop(self):
        self._mqtt_client.publish(self._stop_topic)
        self._started = False

    def toggle(self) -> bool:
        if self._started:
            self.stop()
        else:
            self.start()
        return self._started
