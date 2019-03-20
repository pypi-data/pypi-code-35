from typing import Callable, Any

from rover_position_rjg.data.data_filter import DataFilter


class FilterToggle:
    _filter: DataFilter[Any, Any]

    def __init__(self,
                 root_filter: DataFilter,
                 attachment_filter_name: str,
                 start_callback: Callable[[str], DataFilter[Any, Any]],
                 stop_callback: Callable[[None], None] = None):
        self._root_filter = root_filter
        self._attachment_filter_name = attachment_filter_name
        self._start_callback = start_callback
        self._stop_callback = stop_callback
        self._filter = None
        self.started = False

    def start(self, mqtt_message: str):
        self.stop()
        attachment_filter = self._root_filter.find(self._attachment_filter_name)
        if attachment_filter:
            self._filter = self._start_callback(mqtt_message)
            attachment_filter.add(self._filter)
            self.started = True

    def stop(self):
        if self.started:
            attachment_filter = self._root_filter.find(self._attachment_filter_name)
            if attachment_filter:
                attachment_filter.remove(self._filter)
            self._filter.close()
            self._filter = None
            self.started = False
            if self._stop_callback:
                self._stop_callback()
