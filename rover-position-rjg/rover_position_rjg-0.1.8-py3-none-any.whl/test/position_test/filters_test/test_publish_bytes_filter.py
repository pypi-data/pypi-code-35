import unittest
from unittest.mock import MagicMock, patch

from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.filters.publish_bytes_filter import PublishBytesFilter
from rover_position_rjg.position.filters.publish_filter import *


class PublishBytesFilterTest(unittest.TestCase):
    @patch("rover_position_rjg.mqtt.mqtt_client.MqttClient")
    def test_publishes_data(self, mock_client: MqttClient):
        mock_client.publish = MagicMock()
        # Arrange
        data = Data(bytes("Hello World", "utf-8"), 123)
        receiver = PublishBytesFilter("pub/topic", mock_client)
        # Act
        receiver.receive(data)
        # Assert
        mock_client.publish.assert_called_once_with("pub/topic", data.value)

    @patch("rover_position_rjg.mqtt.mqtt_client.MqttClient")
    @patch("rover_position_rjg.data.data_filter.DataFilter")
    def test_sends_data_to_downstream_filters(self, mock_client: MqttClient, mock_filter: DataFilter[Vector,Vector]):
        mock_filter.receive = MagicMock()
        receiver = PublishBytesFilter("pub/topic", mock_client)
        receiver.add(mock_filter)
        # Act
        data = Data(bytes("A Fish", "utf-8"), 123456)
        receiver.receive(data)
        # Assert
        mock_filter.receive.assert_called_once_with(data)

