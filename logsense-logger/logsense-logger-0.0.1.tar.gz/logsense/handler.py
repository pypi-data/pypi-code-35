from fluent.handler import FluentHandler, FluentRecordFormatter
from fluent.sender import FluentSender
from logsense.sender import LogSenseSender


class LogSenseRecordFormatter(FluentRecordFormatter, object):
    pass


class LogSenseHandler(FluentHandler):
    def __init__(self,
                 logsense_token,
                 assign_default_formatter=True,
                 logsense_host=None,
                 logsense_port=None,
                 timeout=3.0,
                 verbose=False,
                 buffer_overflow_handler=None,
                 msgpack_kwargs=None,
                 nanosecond_precision=False,
                 **kwargs):

        self._logsense_token = logsense_token
        self._logsense_host = logsense_host
        self._logsense_port = logsense_port
        self._sender = None

        if assign_default_formatter:
            self.setDefaultFormatter()

        FluentHandler.__init__(self,
                               'python',
                               host=self._logsense_host,
                               ssl_server_hostname=self._logsense_host,
                               port=self._logsense_port,
                               use_ssl=True,
                               timeout=timeout,
                               verbose=verbose,
                               buffer_overflow_handler=buffer_overflow_handler,
                               msgpack_kwargs=msgpack_kwargs,
                               nanosecond_precision=nanosecond_precision)

    def setDefaultFormatter(self):
        _custom_format = {
            'host': '%(hostname)s',
            'where': '%(module)s.%(funcName)s',
            'type': '%(levelname)s',
            'stack_trace': '%(exc_text)s'
        }
        _formatter = LogSenseRecordFormatter(_custom_format)
        self.setFormatter(_formatter)

    def getSenderClass(self):
        return LogSenseSender

    @property
    def sender(self):
        if self._sender is None:
            self._sender = LogSenseSender(logsense_token=self._logsense_token,
                                          tag='python',
                                          meta={},
                                          logsense_host=self._logsense_host,
                                          logsense_port=self._logsense_port)
        return self._sender
