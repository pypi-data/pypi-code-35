import logging
import sys
import socket
import os

from pythonjsonlogger import jsonlogger


_LOG_LEVEL_CONVERSION = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
        }


class __Logger(object):
    """
    Helper class to initialize loggers and output in json format when specified. It also redirects flask logs so it
    doesn't log as ERROR all the time.
    """
    def __init__(self):
        self.logger = None

    def get_logger(self):
        """
        Get the logger instance
        :return: logger
        :raises: Exception if logger hasn't been initialized
        """
        if self.logger is None:
            raise Exception("Logger has not been initialized")
        return self.logger

    def initialize(self, name, log_level="debug",
                   json_logging=(os.getenv('JSON_LOGGING').lower() in ("true", "t", "1", "y", "yes") if os.getenv('JSON_LOGGING') is not None else True)):
        """
        Initializes logger with given parameters
        :param name: Name of the logger
        :type name: str
        :param log_level: Lowest log level to log. Default is "debug". Options are "debug", "info", "warning", "error"
        :type log_level: str
        :param json_logging: Whether to log in json or not. Options that evaluate to true are ("true", "t", "1", "y", "yes")
                             Default converts value in JSON_LOGGING env var to bool if set else True
        :type json_logging: bool
        :return: None
        :raises: Exception if logger has not been initialized or log_level/json_logging is invalid
        """
        if self.logger is not None:
            raise Exception("Logger has already been initialized")

        if log_level not in _LOG_LEVEL_CONVERSION:
            raise Exception(f"Log level {log_level} is unknown. "
                            f"Valid options include 'debug'', 'info'', 'warning'', 'error'")
        log_level = _LOG_LEVEL_CONVERSION[log_level]

        logger = logging.getLogger(name)
        logger.setLevel(log_level)

        if json_logging:
            formatter = _StackdriverJsonFormatter(timestamp=True)
        else:
            hostname = str(socket.getfqdn())
            formatter = logging.Formatter(hostname + ' - %(asctime)-15s %(name)-5s %(levelname)-8s - %(message)s')

        # STDOUT
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(log_level)
        stdout_handler.addFilter(lambda record: record.levelno <= logging.WARNING)
        logger.addHandler(stdout_handler)
        stdout_handler.setFormatter(formatter)

        # STDERR
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.ERROR)
        logger.addHandler(stderr_handler)
        stderr_handler.setFormatter(formatter)

        # Redirect flask/werkzeug logging so it doesn't go to STDERR all the time.
        flask_logger = logging.getLogger('werkzeug')
        flask_logger.setLevel(logging.ERROR)
        flask_logger.addHandler(stdout_handler)
        flask_logger.addHandler(stderr_handler)

        self.logger = logger


# Taken from https://medium.com/retailmenot-engineering/formatting-python-logs-for-stackdriver-5a5ddd80761c
# and modified to have stack traces in the 'message' field
class _StackdriverJsonFormatter(jsonlogger.JsonFormatter, object):
    def __init__(self, fmt="%(levelname) %(message) %(stacktrace)", style='%', *args, **kwargs):
        jsonlogger.JsonFormatter.__init__(self, fmt=fmt, *args, **kwargs)

    def process_log_record(self, log_record):
        log_record['severity'] = log_record['levelname']
        del log_record['levelname']

        if 'exc_info' in log_record:
            log_record['message'] += '\n' + log_record['exc_info']
            del log_record['exc_info']

        return super(_StackdriverJsonFormatter, self).process_log_record(log_record)


# This is meant to be imported
logger = __Logger()
