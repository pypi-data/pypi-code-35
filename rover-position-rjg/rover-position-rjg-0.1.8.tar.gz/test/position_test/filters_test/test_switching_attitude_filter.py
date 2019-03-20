import math
import unittest
from unittest.mock import patch, MagicMock

from rover_position_rjg.position.filters.attitude_filter import *
from rover_position_rjg.position.filters.switching_attitude_filter import SwitchingAttitudeFilter


class TestAlgorithm(AttitudeAlgorithm):
    def __init__(self, name: str, result: Quaternion = None):
        super().__init__()
        self.name = name
        self.attitude = result
        self.last_timestamp = 0
        self.reset_called = False
        self.requests = []

    def reset(self):
        self.reset_called = True

    def initialise(self, attitude: Quaternion, timestamp: float):
        self.attitude = attitude
        self.last_timestamp = timestamp
        self.initialised = True

    def step(self, data: NineDoFData) -> Quaternion:
        self.requests.append(data)
        self.initialise(self.attitude, data.acceleration.timestamp)
        return self.attitude


class SwitchingAttitudeFilterTest(unittest.TestCase):
    no_acceleration = Vector([0, 0, 1])

    def init_filter(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput], static_attitude: Quaternion = None, dynamic_attitude: Quaternion = None):
        mock_filter.receive = MagicMock()
        self.static_algorithm = TestAlgorithm('static', static_attitude)
        self.dynamic_algorithm = TestAlgorithm('dynamic', dynamic_attitude)
        self.the_filter = SwitchingAttitudeFilter(self.static_algorithm, self.dynamic_algorithm, acceleration_sensitivity=0.01, cool_down=3)
        self.the_filter.add(mock_filter)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_removes_g_from_output(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        attitude = Quaternion(1, 0, 0, 0)
        self.init_filter(mock_filter, attitude)
        # Act
        nine_dof = NineDoFData.zero()
        acceleration = Vector([0, 0, 0.999])
        nine_dof.acceleration.value = acceleration
        data = Data(nine_dof, 456)
        self.the_filter.receive(data)
        # Assert
        self.assert_filter_received(mock_filter, attitude, Vector([0, 0, -0.001]), Flags(0x02))

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_sets_status_flag_if_stationary(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        attitude = Quaternion(1, 0, 0, 0)
        self.init_filter(mock_filter, attitude)
        # Act
        nine_dof = NineDoFData.zero()
        nine_dof.status = Flags(0xF0)
        acceleration = Vector([0, 0, 1])
        nine_dof.acceleration.value = acceleration
        data = Data(nine_dof, 456)
        self.the_filter.receive(data)
        # Assert
        self.assert_filter_received(mock_filter, attitude, Vector.zero(), Flags(0xF2))

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_sets_status_flag_if_moving(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        attitude = Quaternion(1, 0, 0, 0)
        self.init_filter(mock_filter, attitude)
        # Act
        nine_dof = NineDoFData.zero()
        nine_dof.status = Flags(0xF2)
        acceleration = Vector([1, 1, 1])
        nine_dof.acceleration.value = acceleration
        data = Data(nine_dof, 456)
        self.the_filter.receive(data)
        # Assert
        self.assert_filter_received(mock_filter, attitude, Vector([1, 1, 0]), Flags(0xF0))

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_step_calls_static_algorithm_while_acceleration_is_approx_1(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        attitude = Quaternion(0, 0, 1, 0)
        self.init_filter(mock_filter, attitude)
        # Act
        nine_dof = NineDoFData.zero()
        a_z = math.sqrt(1 - 0.1**2 - 0.2**2)
        acceleration = Vector([0.1, 0.2, a_z])
        nine_dof.acceleration.value = acceleration
        data = Data(nine_dof, 456)
        self.the_filter.receive(data)
        # Assert
        self.assert_filters_received_calls(static_filter_call_count=1, dynamic_filter_call_count=0)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_switches_to_dynamic_algorithm_if_acceleration_is_greater_than_trigger(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        attitude = Quaternion(0, 0, 1, 0)
        self.init_filter(mock_filter, None, attitude)
        # Act
        data = self.build_data(1, Vector([0.5, 0.1, 0.9]))
        self.the_filter.receive(data)
        # Assert
        self.assertEqual(self.dynamic_algorithm, self.the_filter.current_algorithm)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_switches_to_dynamic_algorithm_if_acceleration_is_less_than_trigger(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        attitude = Quaternion(0, 0, 1, 0)
        self.init_filter(mock_filter, None, attitude)
        # Act
        nine_dof = NineDoFData.zero()
        acceleration = Vector([0.1, 0.1, 0.3])
        nine_dof.acceleration.value = acceleration
        data = self.build_data(1, acceleration)
        self.the_filter.receive(data)
        # Assert
        self.assertEqual(self.dynamic_algorithm, self.the_filter.current_algorithm)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_does_not_switch_to_dynamic_algorithm_due_to_noise(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        attitude = Quaternion(0, 0, 1, 0)
        self.init_filter(mock_filter, attitude, attitude)
        # Act
        nine_dof = NineDoFData.zero()
        acceleration = Vector([0.05, 0.05, 0.994])
        nine_dof.acceleration.value = acceleration
        data = self.build_data(1, acceleration)
        self.the_filter.receive(data)
        # Assert
        self.assertEqual(self.static_algorithm, self.the_filter.current_algorithm)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_initialises_and_calls_dynamic_algorithm_when_switching_from_static_algorithm(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        static_attitude = Quaternion(0.5, 0.5, 0.5, 0.5)
        dynamic_attitude = Quaternion(1, 0, 0, 0)
        self.init_filter(mock_filter, static_attitude, dynamic_attitude)
        self.the_filter.receive(self.build_data(122))
        # Act
        timestamp = 123
        data = self.build_data(timestamp, Vector([0.5, 0.1, 0.9]))
        self.the_filter.receive(data)
        # Assert
        self.assertEqual(static_attitude, self.dynamic_algorithm.attitude)
        self.assertTrue(self.dynamic_algorithm.initialised)
        self.assertEqual(timestamp, self.dynamic_algorithm.last_timestamp)
        self.assert_filters_received_calls(static_filter_call_count=1, dynamic_filter_call_count=1)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_does_not_switch_to_static_algorithm_after_brief_period_without_acceleration(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        static_attitude = Quaternion(0.5, 0.5, 0.5, 0.5)
        self.init_filter(mock_filter, static_attitude)
        self.the_filter.receive(self.build_data(123, Vector([0.5, 0.1, 0.9])))
        # Act
        self.the_filter.receive(self.build_data(123.1, self.no_acceleration))
        self.the_filter.receive(self.build_data(123.2, self.no_acceleration))
        self.the_filter.receive(self.build_data(123.3, self.no_acceleration))
        # Assert
        self.assertEqual(self.dynamic_algorithm, self.the_filter.current_algorithm)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_switches_to_static_algorithm_when_no_acceleration_for_given_time(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        static_attitude = Quaternion(0.5, 0.5, 0.5, 0.5)
        self.init_filter(mock_filter, static_attitude)
        self.the_filter.receive(self.build_data(123, Vector([0.5, 0.1, 0.9])))
        # Act
        self.the_filter.receive(self.build_data(124, self.no_acceleration))
        self.the_filter.receive(self.build_data(127, self.no_acceleration))
        # Assert
        self.assertEqual(self.static_algorithm, self.the_filter.current_algorithm)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_resets_static_algorithm_when_switching_from_dynamic_algorithm(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        static_attitude = Quaternion(0.5, 0.5, 0.5, 0.5)
        self.init_filter(mock_filter, static_attitude)
        self.the_filter.receive(self.build_data(123, Vector([0.5, 0.1, 0.9])))
        # Act
        self.the_filter.receive(self.build_data(124, self.no_acceleration))
        self.the_filter.receive(self.build_data(127, self.no_acceleration))
        # Assert
        self.assertTrue(self.static_algorithm.reset_called)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_does_not_switch_to_static_algorithm_immediately_after_first_switch(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        static_attitude = Quaternion(0.5, 0.5, 0.5, 0.5)
        self.init_filter(mock_filter, static_attitude)
        # Switch from static to dynamic and back again
        self.the_filter.receive(self.build_data(123, Vector([0.5, 0.1, 0.9])))
        self.the_filter.receive(self.build_data(124, self.no_acceleration))
        self.the_filter.receive(self.build_data(127, self.no_acceleration))
        self.assertEqual(self.static_algorithm, self.the_filter.current_algorithm)
        self.the_filter.receive(self.build_data(128, Vector([0.5, 0.1, 0.9])))
        self.assertEqual(self.dynamic_algorithm, self.the_filter.current_algorithm)
        # Act
        self.the_filter.receive(self.build_data(128.1, self.no_acceleration))
        # Assert
        self.assertEqual(self.dynamic_algorithm, self.the_filter.current_algorithm)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_high_g_resets_cool_down(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        static_attitude = Quaternion(0.5, 0.5, 0.5, 0.5)
        self.init_filter(mock_filter, static_attitude)
        self.the_filter.receive(self.build_data(123, Vector([0.5, 0.1, 0.9])))
        # Act
        self.the_filter.receive(self.build_data(124, self.no_acceleration))
        self.the_filter.receive(self.build_data(127, Vector.one()))
        self.the_filter.receive(self.build_data(128, self.no_acceleration))
        # Assert
        self.assertEqual(self.dynamic_algorithm, self.the_filter.current_algorithm)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_reset_switches_to_static_algorithm(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        static_attitude = Quaternion(0.5, 0.5, 0.5, 0.5)
        self.init_filter(mock_filter, static_attitude)
        self.the_filter.receive(self.build_data(123, Vector([0.5, 0.1, 0.9])))
        self.assertEqual(self.dynamic_algorithm, self.the_filter.current_algorithm)
        # Act
        self.the_filter.reset()
        # Assert
        self.assertEqual(self.static_algorithm, self.the_filter.current_algorithm)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_uses_cooldown_after_switching_to_dynamic_algorithm_after_reset(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        static_attitude = Quaternion(0.5, 0.5, 0.5, 0.5)
        self.init_filter(mock_filter, static_attitude)
        self.the_filter.receive(self.build_data(123, Vector([0.5, 0.1, 0.9])))
        self.the_filter.reset()
        self.the_filter.receive(self.build_data(123, Vector([0.5, 0.1, 0.9])))
        self.assertEqual(self.dynamic_algorithm, self.the_filter.current_algorithm)
        # Act
        self.the_filter.receive(self.build_data(123.1, self.no_acceleration))
        self.the_filter.receive(self.build_data(123.2, self.no_acceleration))
        self.the_filter.receive(self.build_data(123.3, self.no_acceleration))
        # Assert
        self.assertEqual(self.dynamic_algorithm, self.the_filter.current_algorithm)

    @staticmethod
    def build_data(timestamp: float, acc: Vector = no_acceleration, gyro: Vector = Vector.zero(), mag: Vector = Vector.one()):
        nine_dof = NineDoFData(Data(acc, timestamp), Data(gyro, timestamp), Data(mag, timestamp), Data(24, timestamp))
        return Data(nine_dof, 456)

    def assert_filters_received_calls(self, static_filter_call_count: int, dynamic_filter_call_count: int):
        self.assertEqual(static_filter_call_count, len(self.static_algorithm.requests))
        self.assertEqual(dynamic_filter_call_count, len(self.dynamic_algorithm.requests))

    def assert_filter_received(self,
                               mock_filter: DataFilter[AttitudeOutput, AttitudeOutput],
                               attitude: Quaternion,
                               acceleration: Vector,
                               status: Flags,
                               num_calls: int = 1):
        self.assertEqual(num_calls, mock_filter.receive.call_count)
        received_data = mock_filter.receive.mock_calls[0][1][0]
        self.assertEqual(attitude, received_data.value.attitude)
        self.assertEqual(acceleration, received_data.value.acceleration)
        self.assertEqual(status, received_data.value.status)
