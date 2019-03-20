import unittest
from unittest.mock import MagicMock, patch

from rover_position_rjg.clients.monitor.app import App
from rover_position_rjg.clients.monitor.messenger import Messenger
from rover_position_rjg.clients.monitor.presenter import Presenter
from rover_position_rjg.data.flags import Flags
from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.filters.attitude_filter import AttitudeOutput
from rover_position_rjg.position.position.position import Position
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class AppTest(unittest.TestCase):
    @patch('rover_position_rjg.clients.monitor.messenger.Messenger')
    @patch('rover_position_rjg.clients.monitor.presenter.Presenter')
    def test_init_starts_publishing_data(self, mock_presenter: Presenter, mock_messenger: Messenger):
        mock_messenger.start_publishing_data = MagicMock()
        app = App(mock_presenter, mock_messenger)
        mock_messenger.start_publishing_data.assert_called_once_with(
            app._on_raw_data_received,
            app._on_scaled_data_received,
            app._on_attitude_data_received,
            app._on_raw_beacon_data_received,
            app._on_scaled_beacon_data_received,
            app._on_position_data_received,
            app._on_heading_data_received
        )

    @patch('rover_position_rjg.clients.monitor.messenger.Messenger')
    @patch('rover_position_rjg.clients.monitor.presenter.Presenter')
    def test_quit_stops_publishing_data(self, mock_presenter: Presenter, mock_messenger: Messenger):
        mock_messenger.stop_publishing_data = MagicMock()
        app = App(mock_presenter, mock_messenger)
        app.quit()
        mock_messenger.stop_publishing_data.assert_called_once_with()

    @patch('rover_position_rjg.clients.monitor.messenger.Messenger')
    @patch('rover_position_rjg.clients.monitor.presenter.Presenter')
    def test_quit_disconnects_from_mqtt(self, mock_presenter: Presenter, mock_messenger: Messenger):
        mock_messenger.disconnect = MagicMock()
        app = App(mock_presenter, mock_messenger)
        app.quit()
        mock_messenger.disconnect.assert_called_once_with()

    @patch('rover_position_rjg.clients.monitor.messenger.Messenger')
    @patch('rover_position_rjg.clients.monitor.presenter.Presenter')
    def test_updates_raw_imu_data_on_receipt(self, mock_presenter: Presenter, mock_messenger: Messenger):
        mock_presenter.present_imu_data = MagicMock()
        app = App(mock_presenter, mock_messenger)
        data = NineDoFData.zero()
        data.temperature.value = 12.3
        # Act
        app._on_raw_data_received(data)
        # Assert
        self.assertEqual(0, mock_presenter.present_imu_data.call_count)

    @patch('rover_position_rjg.clients.monitor.messenger.Messenger')
    @patch('rover_position_rjg.clients.monitor.presenter.Presenter')
    def test_displays_scaled_imu_data_on_receipt(self, mock_presenter: Presenter, mock_messenger: Messenger):
        mock_presenter.present_imu_data = MagicMock()
        app = App(mock_presenter, mock_messenger)
        data = NineDoFData.zero()
        data.temperature.value = 12.3
        # Act
        app._on_scaled_data_received(data)
        # Assert
        self.assertEqual(1, len(mock_presenter.present_imu_data.mock_calls))
        actual_data = mock_presenter.present_imu_data.mock_calls[0][1][0]
        self.assertEqual(actual_data.actual, data)

    @patch('rover_position_rjg.clients.monitor.messenger.Messenger')
    @patch('rover_position_rjg.clients.monitor.presenter.Presenter')
    def test_displays_heading_data_on_receipt(self, mock_presenter: Presenter, mock_messenger: Messenger):
        mock_presenter.present_heading_data = MagicMock()
        app = App(mock_presenter, mock_messenger)
        data = Vector.one()
        gyro_zero = False
        calibrating = True
        stationary = True
        # Act
        app._on_heading_data_received(data, gyro_zero, calibrating, stationary)
        # Assert
        mock_presenter.present_heading_data.assert_called_once_with(data, gyro_zero, calibrating, stationary)

    @patch('rover_position_rjg.clients.monitor.messenger.Messenger')
    @patch('rover_position_rjg.clients.monitor.presenter.Presenter')
    def test_displays_attitude_data_on_receipt(self, mock_presenter: Presenter, mock_messenger: Messenger):
        mock_presenter.present_attitude_data = MagicMock()
        app = App(mock_presenter, mock_messenger)
        data = AttitudeOutput(Vector.one(), Quaternion.identity(), Flags())
        # Act
        app._on_attitude_data_received(data)
        # Assert
        mock_presenter.present_attitude_data.assert_called_once_with(data)

    @patch('rover_position_rjg.clients.monitor.messenger.Messenger')
    @patch('rover_position_rjg.clients.monitor.presenter.Presenter')
    def test_displays_position_data_on_receipt(self, mock_presenter: Presenter, mock_messenger: Messenger):
        mock_presenter.present_position_data = MagicMock()
        app = App(mock_presenter, mock_messenger)
        data = Position(Quaternion.identity(), Vector.one(), Vector.one(), Vector.one())
        # Act
        app._on_position_data_received(data)
        # Assert
        mock_presenter.present_position_data.assert_called_once_with(data)

    @patch('rover_position_rjg.clients.monitor.messenger.Messenger')
    @patch('rover_position_rjg.clients.monitor.presenter.Presenter')
    def test_displays_raw_beacon_data_on_receipt(self, mock_presenter: Presenter, mock_messenger: Messenger):
        mock_presenter.present_raw_beacon_data = MagicMock()
        app = App(mock_presenter, mock_messenger)
        data = Vector.one()
        # Act
        app._on_raw_beacon_data_received(data)
        # Assert
        mock_presenter.present_raw_beacon_data.assert_called_once_with(data)

    @patch('rover_position_rjg.clients.monitor.messenger.Messenger')
    @patch('rover_position_rjg.clients.monitor.presenter.Presenter')
    def test_displays_scaled_beacon_data_on_receipt(self, mock_presenter: Presenter, mock_messenger: Messenger):
        mock_presenter.present_scaled_beacon_data = MagicMock()
        app = App(mock_presenter, mock_messenger)
        data = Vector.one()
        # Act
        app._on_scaled_beacon_data_received(data)
        # Assert
        mock_presenter.present_scaled_beacon_data.assert_called_once_with(data)


if __name__ == '__main__':
    unittest.main()
