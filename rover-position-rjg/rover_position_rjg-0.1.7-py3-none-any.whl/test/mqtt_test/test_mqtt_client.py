import unittest
import paho.mqtt.client as mqtt
from rover_position_rjg.mqtt.mqtt_client import MqttClient


class MqttClientTest(unittest.TestCase):

    def setUp(self):
        self.count = 0
        self.messages = []

    def increment(self):
        self.count = self.count + 1

    def handle_message(self, message: str):
        self.messages.append(message)

    def test_handles_simpleCallback(self):
        client = MqttClient('mqtt_test', "root")

        client.on('count', self.increment)
        client._on_message(client.client, "", mqtt.MQTTMessage(topic=b"root/count"))

        self.assertEqual(1, self.count)

    def test_handles_callbackWithMessage(self):
        client = MqttClient('mqtt_test', "root")

        client.on_message('count', self.handle_message)
        msg = mqtt.MQTTMessage(topic=b"root/count")
        msg.payload = b"hello"
        client._on_message(client.client, "", msg)

        self.assertEqual(1, len(self.messages))
        self.assertEqual(b'hello', self.messages[0])

    def test_handles_unregistered_topic(self):
        client = MqttClient('mqtt_test', "root")

        client.on('count', self.increment)
        client._on_message(client.client, "", mqtt.MQTTMessage(topic=b"root/not_wanted"))

        self.assertEqual(0, self.count)

    def test_supports_absolute_topics(self):
        client = MqttClient('mqtt_test', "root")

        client.on('//count', self.increment)
        client._on_message(client.client, "", mqtt.MQTTMessage(topic=b"count"))

        self.assertEqual(1, self.count)
