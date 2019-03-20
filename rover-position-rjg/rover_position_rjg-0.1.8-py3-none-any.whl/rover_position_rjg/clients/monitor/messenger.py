from typing import Callable

import jsonpickle
import struct

from rover_position_rjg.clients.monitor.imu_data_model import ImuDataModel
from rover_position_rjg.clients.monitor.message_switch import MessageSwitch
from rover_position_rjg.data.flags import Flags
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.mqtt.mqtt_client import MqttClient
from rover_position_rjg.position.filters.attitude_filter import AttitudeOutput
from rover_position_rjg.position.position.position import Position
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class Messenger:
    _imu_raw_message_callback = ...  # type: Callable[[NineDoFData], None]
    _imu_scaled_message_callback = ...  # type: Callable[[NineDoFData], None]
    _attitude_message_callback = ...  # type: Callable[[AttitudeOutput], None]
    _beacon_raw_callback = ...  # type: Callable[[Vector], None]
    _beacon_scaled_callback = ...  # type: Callable[[Vector], None]
    _position_message_callback = ...  # type: Callable[[Position], None]

    def __init__(self):
        self._imu_data = ImuDataModel()
        self._mqtt_client = MqttClient('calibrate', 'position', 0)
        self._mqtt_client.connect()
        self._pause_imu_switch = MessageSwitch(self._mqtt_client, 'pause', 'resume', '', True)
        self._track_position_switch = MessageSwitch(self._mqtt_client, 'track/stop', 'track/start', '', True)
        # Commands to send MQTT data to this app
        frequency = '{"frequency":3}'
        self._publish_imu_data_switch = MessageSwitch(self._mqtt_client, 'data/publish/stop', 'data/publish/start', frequency, False)
        self._publish_attitude_data_switch = MessageSwitch(self._mqtt_client, 'attitude/publish/stop', 'attitude/publish/start', frequency, False)
        self._publish_beacon_data_switch = MessageSwitch(self._mqtt_client, 'absolute/publish/stop', 'absolute/publish/start', frequency, False)
        self._publish_position_data_switch = MessageSwitch(self._mqtt_client, 'publish/stop', 'publish/start', frequency, False)
        self._publish_heading_data_switch = MessageSwitch(self._mqtt_client, 'heading/stop', 'heading/start', '{"frequency":3}', False)
        # Commands to record data to CSV files
        msg = '{{"duration":60,"filename":"{}"}}'
        self._record_imu_data_switch = MessageSwitch(self._mqtt_client, 'data/record/stop', 'data/record/start', msg.format('imu_data.csv'), False)
        self._record_attitude_data_switch = MessageSwitch(self._mqtt_client, 'attitude/record/stop', 'attitude/record/start', msg.format('attitude_output.csv'), False)
        self._record_beacon_data_switch = MessageSwitch(self._mqtt_client, 'absolute/record/stop', 'absolute/record/start', msg.format('absolute_position_data.csv'), False)
        self._record_position_switch = MessageSwitch(self._mqtt_client, 'record/stop', 'record/start', msg.format('position_output.csv'), False)

    def disconnect(self):
        self._mqtt_client.disconnect()

    def check_messages(self):
        self._mqtt_client.loop()

    def start_publishing_data(self,
                              raw_callback: Callable[[NineDoFData], None],
                              scaled_callback: Callable[[NineDoFData], None],
                              attitude_callback: Callable[[AttitudeOutput], None],
                              raw_beacon_callback: Callable[[Vector], None],
                              scaled_beacon_callback: Callable[[Vector], None],
                              position_callback: Callable[[Position], None],
                              heading_callback: Callable[[Vector, bool, bool, bool], None]):
        """Asks the Pi to publish various data several times a second"""
        # IMU Raw and Scaled data
        self._imu_raw_message_callback = raw_callback
        self._imu_scaled_message_callback = scaled_callback
        self._mqtt_client.on_message('data/imu/raw', self._handle_imu_raw_message)
        self._mqtt_client.on_message('data/imu/scaled', self._handle_imu_scaled_message)
        self._publish_imu_data_switch.start()
        # Output of attitude (Madgwick) filter
        self._attitude_message_callback = attitude_callback
        self._mqtt_client.on_message('data/attitude', self._handle_attitude_message)
        # self._publish_attitude_data_switch.start()
        # Beacon (Decawave) raw and scaled output
        self._beacon_raw_callback = raw_beacon_callback
        self._beacon_scaled_callback = scaled_beacon_callback
        self._mqtt_client.on_message('data/absolute/raw', self._handle_beacon_raw_message)
        self._mqtt_client.on_message('data/absolute/scaled', self._handle_beacon_scaled_message)
        # self._publish_beacon_data_switch.start()
        # Output of position (Kalman) filter
        self._position_message_callback = position_callback
        self._mqtt_client.on_message('data/position', self._handle_position_message)
        # self.toggle_position_publish_position_data()
        self._heading_message_callback = heading_callback
        self._mqtt_client.on_message('//sensor/heading/data', self._handle_heading_message)

    def stop_publishing_data(self):
        """Asks the Pi to stop publishing data """
        self._publish_imu_data_switch.stop()
        self._publish_attitude_data_switch.stop()
        self._publish_beacon_data_switch.stop()
        self._publish_position_data_switch.stop()
        self._publish_heading_data_switch.stop()

    def _handle_imu_raw_message(self, mqtt_message: str):
        data = jsonpickle.decode(mqtt_message)
        self._imu_raw_message_callback(data.value)

    def _handle_imu_scaled_message(self, mqtt_message: str):
        data = jsonpickle.decode(mqtt_message)
        self._imu_scaled_message_callback(data.value)

    def _handle_attitude_message(self, mqtt_message: str):
        data = jsonpickle.decode(mqtt_message)
        self._attitude_message_callback(data.value)

    def _handle_beacon_raw_message(self, mqtt_message: str):
        data = jsonpickle.decode(mqtt_message)
        self._beacon_raw_callback(data.value)

    def _handle_beacon_scaled_message(self, mqtt_message: str):
        data = jsonpickle.decode(mqtt_message)
        self._beacon_scaled_callback(data.value)

    def _handle_position_message(self, mqtt_message: str):
        data = jsonpickle.decode(mqtt_message)
        self._position_message_callback(data.value)

    def _handle_heading_message(self, mqtt_message: str):
        x, y, z, s, t = struct.unpack(">fffBf", bytes(mqtt_message))
        status = Flags(s)
        self._heading_message_callback(Vector([x, y, z]), status[0], status[2], status[1])

    def position_exit(self):
        self._mqtt_client.publish('quit')

    def position_calibrate(self):
        self._mqtt_client.publish('calibrate')

    def toggle_position_pause_imu(self):
        self._pause_imu_switch.toggle()

    def toggle_position_track_position(self):
        if self._track_position_switch.toggle():
            self._publish_attitude_data_switch.start()
            self._publish_position_data_switch.start()
            self._publish_beacon_data_switch.start()
        else:
            self._publish_attitude_data_switch.stop()
            self._publish_position_data_switch.stop()

    def toggle_position_publish_imu_data(self):
        self._publish_imu_data_switch.toggle()

    def toggle_position_publish_attitude_data(self):
        self._publish_attitude_data_switch.toggle()

    def toggle_position_publish_beacon_data(self):
        self._publish_beacon_data_switch.toggle()

    def toggle_position_publish_position_data(self):
        self._publish_position_data_switch.toggle()

    def toggle_position_publish_heading_data(self):
        self._publish_heading_data_switch.toggle()

    def toggle_record_all(self):
        if self._record_imu_data_switch.toggle():
            self._record_attitude_data_switch.start()
            self._record_beacon_data_switch.start()
            self._record_position_switch.start()
        else:
            self._record_attitude_data_switch.stop()
            self._record_beacon_data_switch.stop()
            self._record_position_switch.stop()

    def toggle_record_imu_data(self):
        self._record_imu_data_switch.toggle()

    def toggle_record_beacon_data(self):
        self._record_beacon_data_switch.toggle()

    def toggle_record_attitude_data(self):
        self._record_attitude_data_switch.toggle()

    def toggle_record_position_switch(self):
        self._record_position_switch.toggle()
