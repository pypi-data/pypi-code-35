import curses
from rover_position_rjg.clients.monitor.imu_data_model import ImuDataModel
from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.filters.attitude_filter import AttitudeOutput
from rover_position_rjg.position.position.position import Position
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class View:
    def __init__(self, stdscr):
        self.main_window = stdscr
        self.imu_data_window = curses.newwin(6, 80, 0, 0)
        self.heading_window = curses.newwin(3, 80, 6, 0)
        self.attitude_window = curses.newwin(4, 80, 9, 0)
        self.beacon_window = curses.newwin(4, 80, 13, 0)
        self.output_window = curses.newwin(4, 80, 17, 0)

    def display_template(self):
        self.imu_data_window.addstr(0, 0, '-------------------------------------------------------------------------------')
        self.imu_data_window.addstr(1, 0, 'IMU     Accelerometer    |       Gyroscope      |    Magnetometer      | Temp')
        self.imu_data_window.addstr(2, 0, '       x      y      z   |    x      y      z   |   x      y      z    |')
        self.imu_data_window.addstr(3, 0, 'Raw                      |                      |                      |')
        self.imu_data_window.addstr(4, 0, 'Act                      |                      |                      |')
        self.imu_data_window.addstr(5, 0, 'Mag/Err                  |                      |                      |   NA')
        self.heading_window.addstr(0, 0,  '-------------------------------------------------------------------------------')
        self.heading_window.addstr(1, 0,  'Attitude   Roll  Pitch    Yaw  G-Zero   Cal  Madg')
        self.heading_window.addstr(2, 0,  'Heading')
        self.attitude_window.addstr(0, 0, '-------------------------------------------------------------------------------')
        self.attitude_window.addstr(1, 0, 'Attitude Output (Madgwick)    |            Roll  Pitch    Yaw')
        self.attitude_window.addstr(2, 0, 'Acceler.                      | Heading ')
        self.attitude_window.addstr(3, 0, 'Quatern.')
        self.beacon_window.addstr(0, 0,   '-------------------------------------------------------------------------------')
        self.beacon_window.addstr(1, 0,   'Beacon      x      y      z')
        self.beacon_window.addstr(2, 0,   'Raw')
        self.beacon_window.addstr(3, 0,   'Scaled')
        self.output_window.addstr(0, 0,   '-------------------------------------------------------------------------------')
        self.output_window.addstr(1, 0,   'Position Output (Kalman)')
        self.output_window.addstr(2, 0,   'Acceler.                      | Heading ')
        self.output_window.addstr(3, 0,   'Position                      | Velocity')
        r = self.get_row_after(self.output_window)
        self.main_window.addstr(r, 0,     '-------------------------------------------------------------------------------')
        self.main_window.addstr(r+1, 0,   'Monitor:  (q)uit')
        self.main_window.addstr(r+2, 0,   'Position: (p)ause imu, (t)rack position, (c)alibrate, e(x)it app')
        self.main_window.addstr(r+3, 0,   'Publish:  (i)mu, (a)ttitude, (b)eacon, p(o)sition, (h)eading)')
        self.main_window.addstr(r+4, 0,   'Record:   (0)all, (1)imu, (2)attitude out, (3)beacon, (4)position out')
        self.main_window.addstr(r+5, 0,   '-------------------------------------------------------------------------------')
        self.main_window.refresh()
        self.imu_data_window.refresh()
        self.heading_window.refresh()
        self.attitude_window.refresh()
        self.beacon_window.refresh()
        self.output_window.refresh()

    def display_imu_data(self, imu_data: ImuDataModel):
        self.print_9dof(self.imu_data_window, 3, imu_data.raw, True)
        self.print_9dof(self.imu_data_window, 4, imu_data.actual, False)
        actual_error = imu_data.get_actual_error()
        self.print_mag_error(8, imu_data.actual.acceleration.value.magnitude(), actual_error.x)
        self.print_mag_error(30, imu_data.actual.angular_velocity.value.magnitude(), actual_error.y)
        relative_mag_field = imu_data.get_relative_magnetic_field(imu_data.actual.magnetic_field.value.magnitude())
        relative_mag_error = imu_data.get_relative_magnetic_field(actual_error.z)
        self.print_mag_error(53, relative_mag_field, relative_mag_error)
        self.imu_data_window.refresh()

    def print_mag_error(self, x: int, magnitude: float, error: float):
        self.imu_data_window.addstr(5, x, '{:7.4f} {:7.4f}'.format(magnitude, error))

    def print_9dof(self, window: any, y: int, data: NineDoFData, raw: bool):
        self.print_vector(window, y, 4, data.acceleration.value, raw)
        self.print_vector(window, y, 27, data.angular_velocity.value, raw)
        self.print_vector(window, y, 50, data.magnetic_field.value, raw)
        window.addstr(y, 73, '{:5.0f}'.format(data.temperature.value))

    def display_attitude_data(self, data: AttitudeOutput):
        self.print_vector(self.attitude_window, 2, 9, data.acceleration, False)
        a = data.attitude
        self.print_as_tait_bryan_angles(self.attitude_window, 2, 41, a)
        self.attitude_window.addstr(3, 9, '{:9.6f} {:9.6f} {:9.6f} {:9.6f}'.format(a.w, a.i, a.j, a.k))
        self.attitude_window.refresh()

    def display_raw_beacon_data(self, data: Vector):
        self.print_vector(self.beacon_window, 2, 9, data, False)
        self.beacon_window.refresh()

    def display_scaled_beacon_data(self, data: Vector):
        self.print_vector(self.beacon_window, 3, 9, data, False)
        self.beacon_window.refresh()

    def display_position_data(self, data: Position):
        self.print_vector(self.output_window, 2, 9, data.acceleration, False)
        a = data.attitude
        if a:
            self.print_as_tait_bryan_angles(self.output_window, 2, 41, a)
        if data.position:
            self.print_vector(self.output_window, 3, 9, data.position, False)
        if data.velocity:
            self.print_vector(self.output_window, 3, 41, data.velocity, False)
        self.output_window.refresh()

    def display_heading_data(self, data: Vector, gyro_in_zero_limit: bool, calibrating: bool, stationary: bool):
        self.heading_window.addstr(2, 9, '{:6.1f} {:6.1f} {:6.1f}   {:>5s} {:>5s} {:>5s}'.format(data.x, data.y, data.z, str(gyro_in_zero_limit), str(calibrating), str(stationary)))
        self.heading_window.refresh()

    @staticmethod
    def get_row_after(window: any) -> int:
        return window.getbegyx()[0] + window.getmaxyx()[0]

    @staticmethod
    def print_as_tait_bryan_angles(window: any, y: int, x: int, quaternion: Quaternion):
        e = quaternion.to_tait_bryan()
        window.addstr(y, x, '{:6.1f} {:6.1f} {:6.1f}'.format(e.x, e.y, e.z))

    @staticmethod
    def print_vector(window: any, y: int, x: int, vector: Vector, raw: bool):
        if raw:
            window.addstr(y, x, '{:6.0f} {:6.0f} {:6.0f}'.format(vector.x, vector.y, vector.z))
        else:
            window.addstr(y, x, '{:6.3f} {:6.3f} {:6.3f}'.format(vector.x, vector.y, vector.z))

