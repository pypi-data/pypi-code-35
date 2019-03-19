import numpy as np
from numpy.core.multiarray import ndarray

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.data_filter import DataFilter
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class FrequencyShiftFilter(DataFilter[NineDoFData, NineDoFData]):
    """Reduces the frequency of NineDoFData. i.e. emits data
    less often than it receives it. Each emitted data contains
    the average value of the data that was received since the
    last emission. Handy for logging etc."""
    inputs = ...  # type: ndarray

    def __init__(self, frequency: float):
        super().__init__()
        self.period = 1 / frequency
        self.start: float = None
        self.latest = self.start
        self.clear_inputs()

    def receive(self, data: Data[NineDoFData]) -> None:
        if not self.start:
            self.start = data.timestamp
        due = self.start + self.period
        if data.timestamp > due:
            if data.timestamp > due + self.period:
                # We've been paused for a while. Re-sync start with timestamps
                self.start = data.timestamp
            else:
                self.start = due
            average = self.get_average()
            self.send(average)
            self.clear_inputs()
        acc = data.value.acceleration.value
        gyro = data.value.angular_velocity.value
        mag = data.value.magnetic_field.value
        temp = data.value.temperature.value
        self.inputs = np.append(self.inputs, [[acc.x, acc.y, acc.z, gyro.x, gyro.y, gyro.z, mag.x, mag.y, mag.z, temp]], axis=0)
        self.latest = data.timestamp

    def get_average(self) -> Data[NineDoFData]:
        average = np.average(self.inputs, axis=0)
        acc = Data(Vector([average[0], average[1], average[2]]), self.latest)
        gyro = Data(Vector([average[3], average[4], average[5]]), self.latest)
        mag = Data(Vector([average[6], average[7], average[8]]), self.latest)
        temp = Data(average[9], self.latest)
        nine_dof = NineDoFData(acc, gyro, mag, temp)
        return Data(nine_dof, self.latest)

    def clear_inputs(self):
        self.inputs = np.empty([0, 10])

    def close(self) -> None:
        self.clear_inputs()
