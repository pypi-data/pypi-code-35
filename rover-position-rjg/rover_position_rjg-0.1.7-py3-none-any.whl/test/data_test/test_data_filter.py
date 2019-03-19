import time
import unittest
from unittest.mock import MagicMock, patch

from rover_position_rjg.data.data import *
from rover_position_rjg.data.data_filter import DataFilter


class TestFilter(DataFilter[str, str]):
    def __init__(self, name: str = ''):
        super().__init__(name)

    def receive(self, data: Data[str]) -> None:
        pass


class DataFilterTest(unittest.TestCase):
    def test_filter_has_name(self):
        a_filter = TestFilter('the name')
        # Assert
        self.assertEqual('the name', a_filter.name)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_add_returns_added_filter(self, mock_filter: DataFilter[str, str]):
        a_filter = TestFilter()
        # Act
        result = a_filter.add(mock_filter)
        # Assert
        self.assertIs(mock_filter, result)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_remove_returns_removed_filter(self, mock_filter: DataFilter[str, str]):
        a_filter = TestFilter()
        a_filter.add(mock_filter)
        # Act
        result = a_filter.remove(mock_filter)
        # Assert
        self.assertIs(mock_filter, result)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_send_updates_to_filters(self, mock_filter: DataFilter[str, int], mock_filter2: DataFilter[str, float]):
        mock_filter.receive = MagicMock()
        mock_filter2.receive = MagicMock()
        a_filter = TestFilter()
        a_filter.add(mock_filter)
        a_filter.add(mock_filter2)
        data = Data('message 1', time.time())
        # Act
        a_filter.send(data)
        # Assert
        mock_filter.receive.assert_called_once_with(data)
        mock_filter2.receive.assert_called_once_with(data)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_send_excludes_removed_filters(self, mock_filter: DataFilter[str, int], mock_filter2: DataFilter[str, float]):
        mock_filter.receive = MagicMock()
        mock_filter2.receive = MagicMock()
        a_filter = TestFilter()
        a_filter.add(mock_filter)
        a_filter.add(mock_filter2)
        data = Data('message 1', time.time())
        a_filter.send(data)
        mock_filter.receive.assert_called_once_with(data)
        mock_filter.receive.reset_mock()
        mock_filter2.receive.assert_called_once_with(data)
        mock_filter2.receive.reset_mock()
        # Act
        a_filter.remove(mock_filter2)
        data2 = Data('message 2', time.time())
        a_filter.send(data2)
        mock_filter.receive.assert_called_once_with(data2)
        mock_filter2.receive.assert_not_called()

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_safe_to_remove_not_in_list(self, mock_filter: DataFilter[str, int]):
        a_filter = TestFilter()
        a_filter.add(mock_filter)
        a_filter.remove(mock_filter)
        a_filter.remove(mock_filter)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_close_removes_and_closes_children(self, mock_filter: DataFilter[str, int], mock_filter2: DataFilter[str, float]):
        mock_filter.close = MagicMock()
        mock_filter2.close = MagicMock()
        a_filter = TestFilter()
        a_filter.add(mock_filter)
        a_filter.add(mock_filter2)
        # Act
        a_filter.close()
        # Assert
        mock_filter.close.assert_called_once_with()
        mock_filter2.close.assert_called_once_with()
        self.assertEqual(0, len(a_filter.receivers))

    def test_find_returns_none_if_not_found(self):
        parent = TestFilter('parent')
        parent.add(TestFilter('child 1'))
        # Act
        found = parent.find('not found')
        # Assert
        self.assertIsNone(found)

    def test_find_can_find_parent(self):
        parent = TestFilter('parent')
        # Act
        found = parent.find('parent')
        # Assert
        self.assertEqual(parent, found)

    def test_find_finds_first_child_with_correct_name(self):
        parent = TestFilter('parent')
        grand_child_1 = parent.add(TestFilter('child 1')).add(TestFilter('grand child'))
        parent.add(TestFilter('child 2')).add(TestFilter('grand child'))
        # Act
        found = parent.find('grand child')
        # Assert
        self.assertEqual(grand_child_1, found)


if __name__ == '__main__':
    unittest.main()
