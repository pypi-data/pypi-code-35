from rover_position_rjg.clients.monitor.imu_data_model import ImuDataModel
from rover_position_rjg.clients.monitor.messenger import Messenger
from rover_position_rjg.clients.monitor.presenter import Presenter
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.filters.attitude_filter import AttitudeOutput
from rover_position_rjg.position.position.position import Position
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class App:
    def __init__(self, presenter: Presenter, messenger: Messenger):
        self.imu_data_model = ImuDataModel()
        self._presenter = presenter
        self._messenger = messenger
        self._messenger.start_publishing_data(
            self._on_raw_data_received,
            self._on_scaled_data_received,
            self._on_attitude_data_received,
            self._on_raw_beacon_data_received,
            self._on_scaled_beacon_data_received,
            self._on_position_data_received,
            self._on_heading_data_received)

    def quit(self):
        self._messenger.stop_publishing_data()
        self._messenger.check_messages()
        self._messenger.disconnect()

    def _on_raw_data_received(self, data: NineDoFData):
        self.imu_data_model.raw = data

    def _on_scaled_data_received(self, data: NineDoFData):
        self.imu_data_model.actual = data
        self._presenter.present_imu_data(self.imu_data_model)

    def _on_attitude_data_received(self, data: AttitudeOutput):
        self._presenter.present_attitude_data(data)

    def _on_raw_beacon_data_received(self, data: Vector):
        self._presenter.present_raw_beacon_data(data)

    def _on_scaled_beacon_data_received(self, data: Vector):
        self._presenter.present_scaled_beacon_data(data)

    def _on_position_data_received(self, data: Position):
        self._presenter.present_position_data(data)

    def _on_heading_data_received(self, data: Vector, gyro_in_zero_limit: bool, calibrating: bool, stationary: bool):
        self._presenter.present_heading_data(data, gyro_in_zero_limit, calibrating, stationary)