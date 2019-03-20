import unittest
from unittest.mock import MagicMock, patch

from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.filters.publish_filter import *


class PublishFilterTest(unittest.TestCase):
    def test_json_pickle(self):
        vector = Vector([1, 2, 3])
        data = Data[Vector](vector, 123456)
        json_str = jsonpickle.encode(data)
        obj = jsonpickle.decode(json_str)
        self.assertEqual(obj.timestamp, data.timestamp)
        self.assertTrue(data.value == obj.value)

    @patch('rover_position_rjg.mqtt.mqtt_client.MqttClient')
    def test_publishes_data(self, mock_client: MqttClient):
        mock_client.publish = MagicMock()
        # Arrange
        vector = Vector([1, 2, 3])
        data = Data[Vector](vector, 123456)
        receiver = PublishFilter('pub/topic', mock_client)
        # Act
        receiver.receive(data)
        # Assert
        payload = mock_client.publish.mock_calls[0][1][1]
        mock_client.publish.assert_called_once_with('pub/topic', payload)
        obj = jsonpickle.decode(payload)
        self.assertEqual(obj.timestamp, data.timestamp)
        self.assertTrue(data.value == obj.value)

    @patch('rover_position_rjg.mqtt.mqtt_client.MqttClient')
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_sends_data(self, mock_client: MqttClient, mock_filter: DataFilter[Vector,Vector]):
        mock_filter.receive = MagicMock()
        receiver = PublishFilter[Vector]('pub/topic', mock_client)
        receiver.add(mock_filter)
        # Act
        data = Data[Vector](Vector.zero(), 123456)
        receiver.receive(data)
        # Assert
        mock_filter.receive.assert_called_once_with(data)
