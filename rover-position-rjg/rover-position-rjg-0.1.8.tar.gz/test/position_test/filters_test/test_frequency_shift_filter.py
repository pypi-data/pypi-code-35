import random
import time
import unittest
from unittest.mock import MagicMock, patch
from callee import Matcher
from rover_position_rjg.position.filters.frequency_shift_filter import *


class NineDoFMatcher(Matcher):
    def __init__(self, value: float):
        self.expected = value

    def match(self, data: Data[NineDoFData]):
        return self.expected == data.value.acceleration.value.x and \
               self.expected == data.value.acceleration.value.y and \
               self.expected == data.value.acceleration.value.z and \
               self.expected == data.value.angular_velocity.value.x and \
               self.expected == data.value.angular_velocity.value.y and \
               self.expected == data.value.angular_velocity.value.z and \
               self.expected == data.value.magnetic_field.value.x and \
               self.expected == data.value.magnetic_field.value.y and \
               self.expected == data.value.magnetic_field.value.z


class FrequencyShiftFilterTest(unittest.TestCase):
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_sends_data_at_correct_interval(self, mock_filter: DataFilter[NineDoFData, NineDoFData]):
        mock_filter.receive = MagicMock()
        frequency = 100.0
        shifter = FrequencyShiftFilter(100)
        shifter.add(mock_filter)
        data1 = self.getRandomData()
        data2 = self.getRandomData()
        data2.timestamp = data1.timestamp + (0.5 / frequency)
        data3 = self.getRandomData()
        data3.timestamp = data1.timestamp + (1.1 / frequency)

        shifter.receive(data1)
        shifter.receive(data2)
        mock_filter.receive.assert_not_called()
        shifter.receive(data3)
        self.assertEqual(1, mock_filter.receive.call_count)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_maintains_rhythm_after_pause(self, mock_filter: DataFilter[NineDoFData, NineDoFData]):
        mock_filter.receive = MagicMock()
        shifter = FrequencyShiftFilter(1)
        shifter.add(mock_filter)
        data1 = self.getRandomData()
        data2 = self.getRandomData()
        data2.timestamp = data1.timestamp + 1.1
        data3 = self.getRandomData()
        data3.timestamp = data1.timestamp + 5.1
        data4 = self.getRandomData()
        data4.timestamp = data1.timestamp + 5.2
        data5 = self.getRandomData()
        data5.timestamp = data1.timestamp + 6.3

        shifter.receive(data1)
        mock_filter.receive.assert_not_called()
        shifter.receive(data2)
        self.assertEqual(1, mock_filter.receive.call_count)
        shifter.receive(data3)
        self.assertEqual(2, mock_filter.receive.call_count)
        shifter.receive(data4)
        self.assertEqual(2, mock_filter.receive.call_count)
        shifter.receive(data5)
        self.assertEqual(3, mock_filter.receive.call_count)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_averages_data_values(self, mock_filter: DataFilter[NineDoFData, NineDoFData]):
        mock_filter.receive = MagicMock()
        frequency = 100.0
        shifter = FrequencyShiftFilter(100)
        shifter.add(mock_filter)
        data1 = self.getData(1)
        data2 = self.getData(2)
        data2.timestamp = data1.timestamp + (0.5 / frequency)
        data3 = self.getData(5)
        data3.timestamp = data1.timestamp + (1.1 / frequency)
        # Act
        shifter.receive(data1)
        shifter.receive(data2)
        shifter.receive(data3)
        # Assert
        mock_filter.receive.assert_called_once_with(NineDoFMatcher(value=1.5))

    def getData(self, value: float) -> Data[NineDoFData]:
        acceleration = self.buildVector(value)
        angular_velocity = self.buildVector(value)
        magnetic_field = self.buildVector(value)
        nine_dof = NineDoFData(acceleration, angular_velocity, magnetic_field, Data(random.randrange(100), time.time()))
        return Data(nine_dof, time.time())

    def buildVector(self, value: float) -> Data[Vector]:
        return Data(Vector([value, value, value]), time.time())

    def getRandomData(self) -> Data[NineDoFData]:
        acceleration = self.randomVector()
        angular_velocity = self.randomVector()
        magnetic_field = self.randomVector()
        nine_dof = NineDoFData(acceleration, angular_velocity, magnetic_field, Data(random.randrange(100), time.time()))
        return Data(nine_dof, time.time())

    def randomVector(self) -> Data[Vector]:
        range = 10
        return Data(Vector([random.randrange(range), random.randrange(range), random.randrange(range)]), time.time())


if __name__ == '__main__':
    unittest.main()
