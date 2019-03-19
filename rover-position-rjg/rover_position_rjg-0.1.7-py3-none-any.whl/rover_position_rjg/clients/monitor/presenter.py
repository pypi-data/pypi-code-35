from rover_position_rjg.clients.monitor.imu_data_model import ImuDataModel
from rover_position_rjg.clients.monitor.view import View
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.filters.attitude_filter import AttitudeOutput
from rover_position_rjg.position.position.position import Position


class Presenter:
    def __init__(self, view: View):
        self.view = view
        self.present_imu_data(ImuDataModel())

    def present_imu_data(self, value: ImuDataModel):
        self.view.display_imu_data(value)

    def present_attitude_data(self, value: AttitudeOutput):
        self.view.display_attitude_data(value)

    def present_raw_beacon_data(self, value: Vector):
        self.view.display_raw_beacon_data(value)

    def present_scaled_beacon_data(self, value: Vector):
        self.view.display_scaled_beacon_data(value)

    def present_position_data(self, value: Position):
        self.view.display_position_data(value)

    def present_heading_data(self, value: Vector, gyro_in_zero_limit: bool, calibrating: bool, stationary: bool):
        self.view.display_heading_data(value, gyro_in_zero_limit, calibrating, stationary)
