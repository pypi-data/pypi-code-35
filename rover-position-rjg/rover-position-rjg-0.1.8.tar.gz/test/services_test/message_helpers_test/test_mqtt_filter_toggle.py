import unittest
from unittest.mock import patch, MagicMock

from rover_position_rjg.services.message_helpers.mqtt_filter_toggle import *


class TestMqttFilterToggle(unittest.TestCase):
    @patch('rover_position_rjg.mqtt.mqtt_client.MqttClient')
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_constructor_sets_up_mqtt(self,
                                      mock_client: MqttClient,
                                      mock_root_filter: DataFilter[str, str]):
        mock_client.on = MagicMock()
        mock_client.on_message = MagicMock()
        callback = MagicMock()
        # Act
        toggle = MqttFilterToggle(mock_client, mock_root_filter, 'child', 'stop', 'start', callback.return_value)
        # Assert
        self.assertFalse(toggle.started)
        mock_client.on_message.assert_called_with('start', toggle.start)
        mock_client.on.assert_called_with('stop', toggle.stop)
