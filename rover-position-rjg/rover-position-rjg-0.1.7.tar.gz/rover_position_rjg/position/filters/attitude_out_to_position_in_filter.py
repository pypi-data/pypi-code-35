from rover_position_rjg.data.data import Data
from rover_position_rjg.data.data_filter import DataFilter
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.filters.attitude_filter import AttitudeOutput
from rover_position_rjg.position.position.position_input import PositionInput


class AttitudeOutputToPositionInputFilter(DataFilter[AttitudeOutput, PositionInput]):
    def __init__(self, g: float):
        """
        :param g: Acceleration due to gravity in m/s
        """
        super().__init__()
        self.g = Vector([g, g, g])

    def receive(self, data: Data[AttitudeOutput]) -> None:
        acceleration_in_mps = data.value.acceleration.scale(self.g)
        ao = AttitudeOutput(acceleration_in_mps, data.value.attitude, data.value.status)
        position_input = PositionInput(attitude=Data(ao, data.timestamp))
        self.send(Data(position_input, data.timestamp))
