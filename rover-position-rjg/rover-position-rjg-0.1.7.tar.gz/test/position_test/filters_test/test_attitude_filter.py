import unittest
from unittest.mock import MagicMock, patch

from rover_position_rjg.position.filters.attitude_filter import *
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class TestAlgorithm(AttitudeAlgorithm):
    def __init__(self, result: Quaternion):
        super().__init__()
        self.result = result

    def reset(self):
        pass

    def initialise(self, attitude: Quaternion, timestamp: float):
        self.initialised = True

    def step(self, data: NineDoFData) -> Quaternion:
        return self.result


class AttitudeFilterTest(unittest.TestCase):
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_step_calls_algorithm(self, mock_filter: DataFilter[Vector, Vector]):
        mock_filter.receive = MagicMock()
        attitude = Quaternion(0, 0, 1, 0)
        the_filter = AttitudeFilter(TestAlgorithm(attitude))
        the_filter.add(mock_filter)
        # Act
        nine_dof = NineDoFData.zero()
        acceleration = Vector([11, 22, 33])
        nine_dof.acceleration.value = acceleration
        data = Data(nine_dof, 456)
        the_filter.receive(data)
        # Assert
        self.assertEqual(1, mock_filter.receive.call_count)
        received_data = mock_filter.receive.mock_calls[0][1][0]
        self.assertEqual(received_data.value.attitude, attitude)
        self.assertEqual(received_data.value.acceleration, Vector([-11, 22, -34]))

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_removes_g_from_output(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        mock_filter.receive = MagicMock()
        attitude = Quaternion(1, 0, 0, 0)
        the_filter = AttitudeFilter(TestAlgorithm(attitude))
        the_filter.add(mock_filter)
        # Act
        nine_dof = NineDoFData.zero()
        acceleration = Vector([0, 0, 1.5])
        nine_dof.acceleration.value = acceleration
        data = Data(nine_dof, 456)
        the_filter.receive(data)
        # Assert
        self.assertEqual(1, mock_filter.receive.call_count)
        received_data = mock_filter.receive.mock_calls[0][1][0]
        self.assertEqual(received_data.value.attitude, attitude)
        self.assertEqual(received_data.value.acceleration, Vector([0, 0, 0.5]))

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_copies_status_to_output(self, mock_filter: DataFilter[AttitudeOutput, AttitudeOutput]):
        mock_filter.receive = MagicMock()
        the_filter = AttitudeFilter(TestAlgorithm(Quaternion.identity()))
        the_filter.add(mock_filter)
        # Act
        nine_dof = NineDoFData.zero()
        nine_dof.status = Flags(0xA9)
        data = Data(nine_dof, 456)
        the_filter.receive(data)
        # Assert
        received_data = mock_filter.receive.mock_calls[0][1][0]
        self.assertEqual(received_data.value.status, Flags(0xA9))
