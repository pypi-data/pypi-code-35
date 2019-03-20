from fluent.sender import FluentSender
from os import getenv
import logging
import socket


class LogSenseSender:
    def __init__(self,
                 logsense_token=None,
                 tag='python',
                 meta={},
                 logsense_host=None,
                 logsense_port=None,
                 verbose=False,
                 nanosecond_precision = False):
        internal_logger = logging.getLogger('logsense.sender')
        self._logsense_token = logsense_token

        if logsense_host:
            self._logsense_host = logsense_host
        else:
            self._logsense_host = getenv('LOGSENSE_HOST', 'logs.logsense.com')

        if logsense_port:
            self._logsense_port = logsense_port
        else:
            self._logsense_port = int(getenv('LOGSENSE_PORT', '32714'))

        if self._logsense_token is None:
            self._logger = None
            print("LOGSENSE_TOKEN not set - skipping handler")
        else:
            self._verbose = verbose
            self._logger = FluentSender(tag,
                                        host=self._logsense_host,
                                        ssl_server_hostname=self._logsense_host,
                                        port=self._logsense_port,
                                        use_ssl=True,
                                        verbose=self._verbose)

            self._base_dict = self.update_meta(meta)

        self.nanosecond_precision = nanosecond_precision

    def update_meta(self, new_meta):
        self._base_dict = {**new_meta, **{
            'cs_customer_token': self._logsense_token,
            'cs_hostname': socket.gethostname(),
            'cs_pattern_key': 'message'
        }}
        return self._base_dict

    def _convert_value_to_known_type(self, value):
        if isinstance(value, str):
            return value
        elif isinstance(value, int):
            return value
        elif isinstance(value, float):
            return value
        elif isinstance(value, dict):
            return value
        elif isinstance(value, list):
            return value
        else:
            # This fixes issues with e.g. NumPy serialization
            return str(value)

    def emit(self, data={}):
        if self._logger:
            if isinstance(data, dict):
                converted_data = {key: self._convert_value_to_known_type(value) for key, value in data.items()}
            else:
                converted_data = {'message': str(data)}
            self._logger.emit('tag', {**converted_data, **self._base_dict})

    def emit_with_time(self, label, timestamp, data):
        if self._logger:
            if isinstance(data, dict):
                converted_data = {key: self._convert_value_to_known_type(value) for key, value in data.items()}
            else:
                converted_data = {'message': str(data)}
            self._logger.emit_with_time(label, timestamp, {**converted_data, **self._base_dict})

    @property
    def last_error(self):
        if self._logger:
            return self._logger.last_error()
        else:
            return None

    @last_error.setter
    def last_error(self, err):
        if self._logger:
            self._logger.last_error(err)

    def clear_last_error(self, _thread_id=None):
        if self._logger:
            self._logger.clear_last_error(_thread_id)

    def close(self):
        if self._logger:
            self._logger.close()
