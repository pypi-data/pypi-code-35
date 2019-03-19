import time

from rover_position_rjg.data.data_pump.data_provider import DataProvider
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData
from rover_position_rjg.data.data import Data
from lsm9ds1_rjg import Driver, I2CTransport, SPITransport


class ImuDataProvider(DataProvider[NineDoFData]):
    PIN_INT1_AG = 23

    def __init__(self, driver: Driver):
        super().__init__()
        self.driver = driver
        if not self.driver:
            self.driver = Driver(
                # I2CTransport(1, I2CTransport.I2C_AG_ADDRESS, self.PIN_INT1_AG),
                # I2CTransport(1, I2CTransport.I2C_MAG_ADDRESS))
                SPITransport(0, False, self.PIN_INT1_AG),
                SPITransport(1, True),
                high_priority=True)
        self.driver.configure()
        self.data_ready_timestamp = 0

    def get(self) -> Data[NineDoFData]:
        ag_timestamp = self.data_ready_timestamp
        temp, acc, gyro = self.driver.read_ag_data()
        mag_timestamp = self.time()
        mag = self.driver.read_magnetometer()
        nine_dof = NineDoFData(
            Data(Vector(acc), ag_timestamp),
            Data(Vector(gyro), ag_timestamp),
            Data(Vector(mag), mag_timestamp),
            Data(temp, ag_timestamp))
        return Data(nine_dof, self.time())

    def poll(self, timeout: float) -> bool:
        # Wait for acceleration and gyro to be ready.
        # Assume magnetometer will be ready at the same time.
        # This requires that the mag is configured to be faster
        # than the ag ODR
        ready = self.driver.ag_data_ready(int(timeout * 1000))
        if ready:
            # Get the timestamp now to eliminate the time to call get()
            self.data_ready_timestamp = self.time()
        else:
            print("IMU data not ready after {} seconds".format(timeout))
        return ready

    def close(self):
        self.driver.close()

    @staticmethod
    def time():
        return time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW) * 1e-9