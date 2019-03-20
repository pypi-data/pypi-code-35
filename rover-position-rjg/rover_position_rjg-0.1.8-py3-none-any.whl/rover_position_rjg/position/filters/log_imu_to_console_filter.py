import time

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.data_filter import DataFilter
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class LogToConsoleImuDataFilter(DataFilter[NineDoFData, NineDoFData]):
    def __init__(self):
        super().__init__()
        self.start = time.time()

    def receive(self, data: Data[NineDoFData]) -> None:
        acc = data.value.acceleration.value
        dps = data.value.angular_velocity.value
        mag = data.value.magnetic_field.value
        acc_time = data.value.acceleration.timestamp - self.start
        temp = data.value.temperature
        print("dv{}, dps{}, mag{}, time {:5f}, temp {}".format(
            [acc.x, acc.y, acc.z],
            [dps.x, dps.y, dps.z],
            [mag.x, mag.y, mag.z],
            acc_time,
            temp.value))
        self.send(data)

    def close(self):
        # Nothing to do
        pass
