import unittest
from unittest.mock import patch, MagicMock

from rover_position_rjg.services.message_helpers.filter_toggle import *


class TestFilterToggle(unittest.TestCase):
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_start_creates_and_attaches_filter(self,
                                               mock_root_filter: DataFilter[str, str],
                                               mock_attachment_filter: DataFilter[str, str],
                                               mock_filter: DataFilter[str, str]):
        mock_root_filter.find = MagicMock(return_value=mock_attachment_filter)
        mock_attachment_filter.add = MagicMock(return_value=mock_filter)
        start_callback = MagicMock(return_value=mock_filter)
        toggle = FilterToggle(mock_root_filter, 'child', start_callback)
        # Act
        toggle.start('f=3')
        # Assert
        mock_root_filter.find.assert_called_once_with('child')
        start_callback.assert_called_once_with('f=3')
        mock_attachment_filter.add.assert_called_once_with(mock_filter)
        self.assertTrue(toggle.started)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_start_does_nothing_if_attachment_is_not_found(self,
                                                           mock_root_filter: DataFilter[str, str]):
        mock_root_filter.find = MagicMock(return_value=None)
        start_callback = MagicMock()
        toggle = FilterToggle(mock_root_filter, 'child', start_callback)
        # Act
        toggle.start('f=3')
        # Assert
        mock_root_filter.find.assert_called_once_with('child')
        start_callback.assert_not_called()
        self.assertFalse(toggle.started)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_stop_detaches_filter_and_cleans_up(self,
                                                mock_root_filter: DataFilter[str, str],
                                                mock_attachment_filter: DataFilter[str, str],
                                                mock_filter: DataFilter[str, str]):
        mock_root_filter.find = MagicMock(return_value=mock_attachment_filter)
        mock_attachment_filter.add = MagicMock(return_value=mock_filter)
        mock_attachment_filter.remove = MagicMock(return_value=mock_filter)
        start_callback = MagicMock(return_value=mock_filter)
        mock_filter.close = MagicMock()
        toggle = FilterToggle(mock_root_filter, 'child', start_callback)
        toggle.start('f=1')
        # Act
        toggle.stop()
        # Assert
        mock_root_filter.find.assert_called_with('child')
        mock_attachment_filter.remove.assert_called_once_with(mock_filter)
        mock_filter.close.assert_called_once()
        self.assertFalse(toggle.started)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_stop_does_not_detach_if_attachment_is_missing(self,
                                                          mock_root_filter: DataFilter[str, str],
                                                          mock_attachment_filter: DataFilter[str, str],
                                                          mock_filter: DataFilter[str, str]):
        mock_root_filter.find = MagicMock(return_value=mock_attachment_filter)
        mock_attachment_filter.add = MagicMock(return_value=mock_filter)
        mock_attachment_filter.remove = MagicMock(return_value=mock_filter)
        start_callback = MagicMock(return_value=mock_filter)
        mock_filter.close = MagicMock()
        toggle = FilterToggle(mock_root_filter, 'child', start_callback)
        toggle.start('f=1')
        mock_root_filter.find = MagicMock(return_value=None)
        # Act
        toggle.stop()
        # Assert
        mock_root_filter.find.assert_called_with('child')
        mock_attachment_filter.remove.assert_not_called()
        mock_filter.close.assert_called_once()
        self.assertFalse(toggle.started)

    @patch('rover_position_rjg.data.data_filter.DataFilter')
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    @patch('rover_position_rjg.data.data_filter.DataFilter')
    def test_stop_call_stop_callback(self,
                                     mock_root_filter: DataFilter[str, str],
                                     mock_attachment_filter: DataFilter[str, str],
                                     mock_filter: DataFilter[str, str]):
        mock_root_filter.find = MagicMock(return_value=mock_attachment_filter)
        mock_attachment_filter.add = MagicMock(return_value=mock_filter)
        mock_attachment_filter.remove = MagicMock(return_value=mock_filter)
        start_callback = MagicMock(return_value=mock_filter)
        stop_callback = MagicMock()
        mock_filter.close = MagicMock()
        toggle = FilterToggle(mock_root_filter, 'child', start_callback, stop_callback)
        toggle.start('f=1')
        # Act
        toggle.stop()
        # Assert
        stop_callback.assert_called_once()

