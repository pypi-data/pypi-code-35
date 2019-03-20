import json
from multiprocessing.connection import wait
from typing import List

from decawave_1001_rjg import DwmLocationResponse

from rover_position_rjg.csv_helpers.attitude_output_csv_converter import AttitudeOutputCsvConverter
from rover_position_rjg.csv_helpers.data_csv_converter import DataCsvConverter
from rover_position_rjg.csv_helpers.position_csv_converter import PositionCsvConverter
from rover_position_rjg.data.data_pump.data_pump import DataPump
from rover_position_rjg.position.attitude.modified_madgwick import ModifiedMadgwick
from rover_position_rjg.position.attitude.simple_attitude_algorithm import SimpleAttitudeAlgorithm
from rover_position_rjg.position.calibration.decawave.decawave_range_scaler import DecawaveRangeScaler
from rover_position_rjg.position.calibration.imu.imu_scaler import ImuScaler
from rover_position_rjg.position.calibration.rotation_scaler import RotationScaler
from rover_position_rjg.position.filters.attitude_filter import AttitudeOutput
from rover_position_rjg.position.filters.attitude_out_to_position_in_filter import AttitudeOutputToPositionInputFilter
from rover_position_rjg.position.filters.attitude_to_heading_bytes_filter import AttitudeToHeadingBytesFilter
from rover_position_rjg.position.filters.decawave_to_position_in_filter import DecawaveToPositionInputFilter
from rover_position_rjg.position.filters.decawave_trilateration_filter import DecawaveTrilaterationFilter
from rover_position_rjg.position.filters.dwm_location_response_to_vector_filter import DwmLocationResponseToVectorFilter
from rover_position_rjg.position.filters.fan_out_filter import FanOutFilter
from rover_position_rjg.position.filters.frequency_shift_filter import FrequencyShiftFilter
from rover_position_rjg.position.filters.position_filter import PositionFilter
from rover_position_rjg.position.filters.publish_bytes_filter import PublishBytesFilter
from rover_position_rjg.position.filters.sampling_filter import SamplingFilter
from rover_position_rjg.position.filters.scaling_filter import ScalingFilter
from rover_position_rjg.position.filters.switching_attitude_filter import SwitchingAttitudeFilter, SwitchingAttitudeFilterConfig
from rover_position_rjg.position.position.kalman_position_algorithm import KalmanPositionAlgorithm, KalmanPositionAlgorithmConfig
from rover_position_rjg.position.position.position import *
from rover_position_rjg.position.filters.to_csv_filter import ToCsvFilter
from rover_position_rjg.position.filters.publish_filter import PublishFilter
from rover_position_rjg.sensors.decawave.csv.dwm_location_response_to_csv import DwmLocationResponseCsvConverter
from rover_position_rjg.sensors.imu.nine_dof_data_to_csv import *
from rover_position_rjg.services.message_helpers.mqtt_filter_toggle import *


class PositionService:
    _mqtt_client: MqttClient
    _imu_scaler: ImuScaler
    _nine_dof_filters: DataFilter[NineDoFData, NineDoFData]
    _decawave_filters: DataFilter[DwmLocationResponse, DwmLocationResponse]
    _heading_filter: ScalingFilter[NineDoFData]
    _attitude_filter: SwitchingAttitudeFilter
    _tracking_filter: ScalingFilter[NineDoFData]
    _decawave_position_filter: DataFilter[DwmLocationResponse, DwmLocationResponse]

    def __init__(self,
                 g: float,
                 switching_attitude_filter_config: SwitchingAttitudeFilterConfig,
                 kalman_config: KalmanPositionAlgorithmConfig,
                 imu_calibration_filename,
                 decawave_calibration_filename,
                 decawave_range_scaler: DecawaveRangeScaler,
                 decawave_temp: float,
                 nine_dof_data_pump: DataPump[NineDoFData],
                 decawave_data_pump: DataPump[DwmLocationResponse],
                 mqtt_client: MqttClient):
        self._g = g
        self._switching_attitude_filter_config = switching_attitude_filter_config
        self._kalman_config = kalman_config
        self._imu_calibration_filename = imu_calibration_filename
        self._decawave_calibration_filename = decawave_calibration_filename
        self.decawave_range_scaler = decawave_range_scaler
        self.decawave_temp = decawave_temp
        self._nine_dof_data_pump = nine_dof_data_pump
        self._decawave_data_pump = decawave_data_pump
        self._pumps: List[DataPump] = []
        self._mqtt_client = mqtt_client
        self._running = False
        self._paused = False
        self._nine_dof_filters = FanOutFilter[NineDoFData]()
        self._decawave_filters = FanOutFilter[DwmLocationResponse]()
        self._tracking_filter = None
        self._decawave_position_filter = None
        self._apply_calibration()

    def _apply_calibration(self):
        self._imu_scaler = ImuScaler()
        self._decawave_scaler = RotationScaler(Quaternion.identity())
        self.load_calibration()

    def run(self) -> int:
        try:
            if self._nine_dof_data_pump:
                self._pumps.append(self._nine_dof_data_pump)
            if self._decawave_data_pump:
                self._pumps.append(self._decawave_data_pump)

            # Start the data pumps before we have any other threads
            # as multi-threading can cause problems with spawn
            for pump in self._pumps:
                pump.run()

            # Register MQTT callbacks
            self._init_mqtt()

            # Immediately calibrate and start tracking our attitude
            self.track_heading()
            self.calibrate()

            # Record initial IMU data
            # self._record_imu_data.start('{"duration":10}')

            self._running = True
            print("    started running")
            while self._running:
                try:
                    self._mqtt_client.loop()
                    self.receive()
                except (KeyboardInterrupt, SystemExit):
                    self.quit()
        finally:
            # Clean up
            self._nine_dof_filters.close()
            self._decawave_filters.close()
            self._mqtt_client.disconnect()
            for pump in self._pumps:
                pump.halt()
            print("   stopped running")
        return 0

    def receive(self):
        ready_pumps = wait(self._pumps, timeout=0.1)
        if self._decawave_data_pump in ready_pumps:
            data = self._decawave_data_pump.recv()
            if not self._paused:
                self._decawave_filters.receive(data)
            # else just discard the data when paused
        if self._nine_dof_data_pump in ready_pumps:
            data = self._nine_dof_data_pump.recv()
            if not self._paused:
                self._nine_dof_filters.receive(data)
            # else just discard the data when paused

    def _init_mqtt(self):
        self._mqtt_client.connect()
        self._mqtt_client.on('quit', self.quit)
        self._mqtt_client.on('pause', self.pause)
        self._mqtt_client.on('resume', self.resume)
        self._mqtt_client.on('calibrate', self.calibrate)
        self._mqtt_client.on('track/start', self.track_position)
        self._mqtt_client.on('track/stop', self.stop_tracking_position)
        self._mqtt_client.on('imu/calibration/save', self.save_calibration)
        self._mqtt_client.on('imu/calibration/load', self.load_calibration)
        # Log data to disk for later analysis. Off by default.
        self._record_imu_data = MqttFilterToggle(self._mqtt_client, self._nine_dof_filters, '',
            'data/record/stop', 'data/record/start', self.record_imu_data)
        self._record_attitude_data = MqttFilterToggle(self._mqtt_client, self._nine_dof_filters, 'attitude',
            'attitude/record/stop', 'attitude/record/start', self.record_attitude_output)
        self._record_decawave_data = MqttFilterToggle(self._mqtt_client, self._decawave_filters, '',
            'absolute/record/stop', 'absolute/record/start', self.record_decawave_data)
        self._record_position_data = MqttFilterToggle(self._mqtt_client, self._nine_dof_filters, 'position',
            'record/stop', 'record/start', self.record_position_output)
        # MQTT publishers that send data to the monitor app. Off by default.
        self._publish_imu_data_toggle = MqttFilterToggle(self._mqtt_client, self._nine_dof_filters, '',
            'data/publish/stop', 'data/publish/start', self.build_imu_data_publisher)
        self._publish_attitude_data_toggle = MqttFilterToggle(self._mqtt_client, self._nine_dof_filters, 'attitude',
            'attitude/publish/stop', 'attitude/publish/start', self.build_attitude_data_publisher)
        self._publish_decawave_scaled_data_toggle = FilterToggle(
            self._decawave_filters, 'scaled_decawave', self.build_scaled_decawave_data_publisher)
        self._publish_decawave_raw_data_toggle = MqttFilterToggle(self._mqtt_client, self._decawave_filters, 'vector_decawave',
            'absolute/publish/stop', 'absolute/publish/start',
            self.build_raw_decawave_data_publisher, self._publish_decawave_scaled_data_toggle.stop)
        self._publish_position_data_toggle = MqttFilterToggle(self._mqtt_client, self._nine_dof_filters, 'position',
            'publish/stop', 'publish/start', self.build_position_data_publisher)
        # MQTT publishers for specific challenges
        self._publish_heading_toggle = MqttFilterToggle(self._mqtt_client, self._nine_dof_filters, 'attitude',
            'heading/stop', 'heading/start', self.build_heading_data_publisher)

    def quit(self):
        self._running = False

    def pause(self):
        for pump in self._pumps:
            pump.pause()
        self._paused = True
        print("    paused")

    def resume(self):
        """Starts pumping data again and automatically puts the system
        in the state it would have if it had just started."""
        for pump in self._pumps:
            pump.resume()
        self._paused = False
        print("    resumed")
        self.calibrate()

    def calibrate(self):
        print("    calibrating")
        self._attitude_filter.reset()
        self._imu_scaler.calibrate()

    def track_heading(self):
        self._heading_filter = self._nine_dof_filters.add(ScalingFilter(self._imu_scaler))
        self._attitude_filter = SwitchingAttitudeFilter(
            ModifiedMadgwick(),
            SimpleAttitudeAlgorithm(),
            self._switching_attitude_filter_config.acceleration_sensitivity,
            self._switching_attitude_filter_config.cool_down,
            name='attitude')
        self._heading_filter.add(self._attitude_filter)

    def track_position(self):
        """Starts or restarts tracking the rover's position"""
        self.stop_tracking_position()
        position_algorithm = KalmanPositionAlgorithm(
            self._kalman_config.expected_frequency,
            self._kalman_config.mean_position_error,
            self._kalman_config.mean_velocity_error,
            self._kalman_config.mean_acceleration_error)
        position_filter = PositionFilter(position_algorithm, 'position')
        self._tracking_filter = AttitudeOutputToPositionInputFilter(self._g)
        self._tracking_filter.add(position_filter)
        self._heading_filter.find('attitude').add(self._tracking_filter)
        # Setup Decawave filter stack
        trilateration_filter = DecawaveTrilaterationFilter(self.decawave_range_scaler, 'trilateration')
        trilateration_filter.set_temperatures(self.decawave_temp, self.decawave_temp)
        self._decawave_position_filter = trilateration_filter
        self._decawave_filters\
            .add(self._decawave_position_filter) \
            .add(DwmLocationResponseToVectorFilter('vector_decawave'))\
            .add(ScalingFilter(self._decawave_scaler, 'scaled_decawave'))\
            .add(DecawaveToPositionInputFilter())\
            .add(position_filter)

    def stop_tracking_position(self):
        if self._tracking_filter:
            self._publish_position_data_toggle.stop()
            self._publish_decawave_scaled_data_toggle.stop()
            self._heading_filter.remove(self._tracking_filter).close()
            self._tracking_filter = None
            self._decawave_filters.remove(self._decawave_position_filter).close()
            self._decawave_position_filter = None

    def save_calibration(self):
        self._imu_scaler.save(self._imu_calibration_filename)

    def load_calibration(self):
        self._imu_scaler.load(self._imu_calibration_filename)
        self._decawave_scaler.load(self._decawave_calibration_filename)

    @staticmethod
    def record_imu_data(mqtt_message: str) -> DataFilter[NineDoFData, NineDoFData]:
        return PositionService.record(mqtt_message, 'imu_data.csv', NineDoFDataCsvConverter())

    @staticmethod
    def record_attitude_output(mqtt_message: str) -> DataFilter[AttitudeOutput, AttitudeOutput]:
        return PositionService.record(mqtt_message, 'attitude_output.csv', AttitudeOutputCsvConverter())

    @staticmethod
    def record_decawave_data(mqtt_message: str) -> DataFilter[Vector, Vector]:
        return PositionService.record(mqtt_message, 'absolute_position_data.csv', DwmLocationResponseCsvConverter())

    @staticmethod
    def record_position_output(mqtt_message: str) -> DataFilter[Position, Position]:
        return PositionService.record(mqtt_message, 'position_output.csv', PositionCsvConverter())

    @staticmethod
    def record(mqtt_message: str, default_filename: str, converter: CsvConverter):
        payload = json.loads(mqtt_message)
        duration = payload.get('duration', 10)
        filename = payload.get('filename', default_filename)
        converter = DataCsvConverter(converter)
        return ToCsvFilter(converter, filename, duration)

    def build_imu_data_publisher(self, mqtt_message: str) -> DataFilter[NineDoFData, NineDoFData]:
        frequency = self.get_requested_frequency(mqtt_message)
        result = FrequencyShiftFilter(frequency)
        result.add(PublishFilter('data/imu/raw', self._mqtt_client))
        result.add(ScalingFilter(self._imu_scaler))\
              .add(PublishFilter('data/imu/scaled', self._mqtt_client))
        return result

    def build_attitude_data_publisher(self, mqtt_message: str) -> DataFilter[AttitudeOutput, AttitudeOutput]:
        frequency = self.get_requested_frequency(mqtt_message)
        result = SamplingFilter[AttitudeOutput](frequency)
        result.add(PublishFilter('data/attitude', self._mqtt_client))
        return result

    def build_heading_data_publisher(self, mqtt_message: str) -> DataFilter[AttitudeOutput, AttitudeOutput]:
        frequency = self.get_requested_frequency(mqtt_message)
        payload = json.loads(mqtt_message)
        publish_topic = payload.get('topic', '//sensor/heading/data')
        result = SamplingFilter[AttitudeOutput](frequency)
        result.add(AttitudeToHeadingBytesFilter())\
              .add(PublishBytesFilter(publish_topic, self._mqtt_client))
        return result

    def build_raw_decawave_data_publisher(self, mqtt_message: str) -> DataFilter[Vector, Vector]:
        self._publish_decawave_scaled_data_toggle.start(mqtt_message)
        frequency = self.get_requested_frequency(mqtt_message)
        result = SamplingFilter[Vector](frequency)
        result.add(PublishFilter('data/absolute/raw', self._mqtt_client))
        return result

    def build_scaled_decawave_data_publisher(self, mqtt_message: str) -> DataFilter[Vector, Vector]:
        frequency = self.get_requested_frequency(mqtt_message)
        result = SamplingFilter[Vector](frequency)
        result.add(PublishFilter('data/absolute/scaled', self._mqtt_client))
        return result

    def build_position_data_publisher(self, mqtt_message: str) -> DataFilter[Position, Position]:
        frequency = self.get_requested_frequency(mqtt_message)
        result = SamplingFilter[Position](frequency)
        result.add(PublishFilter('data/position', self._mqtt_client))
        return result

    @staticmethod
    def get_requested_frequency(mqtt_message: str):
        payload = json.loads(mqtt_message)
        return payload.get('frequency', 1)
