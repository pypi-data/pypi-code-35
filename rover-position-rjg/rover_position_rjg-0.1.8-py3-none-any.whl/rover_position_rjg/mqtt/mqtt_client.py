import time
from typing import *
import paho.mqtt.client as mqtt


class MqttClient:
    callbacks = ...  # type: Dict[str, Callable[[str], None]]
    simple_callbacks = ...  # type: Dict[str, Callable]

    def __init__(self, client_id: str, root_topic: str, min_loop_interval: float = 0.3):
        self.client_id = client_id
        self.root_topic = root_topic
        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.simple_callbacks = {}
        self.callbacks = {}
        self.min_loop_interval = min_loop_interval # In seconds
        self.last_loop_time = time.time()

    def connect(self):
        self.client.connect('localhost')

    def disconnect(self):
        self.client.disconnect()

    def publish(self, topic: str, payload: str = None):
        self.client.publish(self._build_topic(topic), payload)

    def loop(self):
        """A single check to mqtt.loop() takes 0.1 to 0.2 ms
        which becomes onerous at high frequencies. This version
        limits the number of calls per second."""
        current_time = time.time()
        if current_time - self.last_loop_time >= self.min_loop_interval:
            self.client.loop(0)
            self.last_loop_time = current_time

    def _build_topic(self, topic: str):
        if topic.startswith('//'):
            return topic[2:]
        return '{}/{}'.format(self.root_topic, topic)

    def on(self, topic: str, callback: Callable):
        full_topic = self._build_topic(topic)
        self.simple_callbacks[full_topic] = callback
        self.client.subscribe(full_topic)

    def on_message(self, topic: str, callback: Callable[[str], None]):
        full_topic = self._build_topic(topic)
        self.callbacks[full_topic] = callback
        self.client.subscribe(full_topic)

    def _on_message(self, client: mqtt.Client, userdata: str, msg: mqtt.MQTTMessage):
        topic = msg.topic
        simple_callback = self.simple_callbacks.get(topic, None)
        if simple_callback:
            simple_callback()
        message_handler = self.callbacks.get(topic, None)
        if message_handler:
            message_handler(msg.payload)

    def _on_connect(self, client: mqtt.Client, userdata, flags, rc: int):
        if rc == mqtt.MQTT_ERR_SUCCESS:
            # print('{} connected to MQTT'.format(self.client_id))
            pass
        else:
            print('{} failed to connect to MQTT. ({})'.format(self.client_id, mqtt.connack_string(rc)))

    def _on_disconnect(self, client: mqtt.Client, userdata: str, rc: int):
        if rc != mqtt.MQTT_ERR_SUCCESS:
            print('{} disconnected unexpectedly from MQTT. Reconnecting.'.format(self.client_id))
            self.client.reconnect()
        else:
            print('{} disconnected from MQTT.'.format(self.client_id))
