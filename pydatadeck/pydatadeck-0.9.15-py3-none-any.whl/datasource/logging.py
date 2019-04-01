"""Logging related classes and functions"""

import json
import logging
from datetime import datetime
from urllib.parse import urlparse

from flask import g, request


class RequestFormatter(logging.Formatter):
    """
    Log record formatter which prepends log messages with timestamp, trace_id,
    HTTP method and request path
    """

    def __init__(self, logFormat=None, timeFormat=None,
                 json_output=False, service_name='Undefined'):
        super(RequestFormatter, self).__init__(logFormat, timeFormat)
        self.json_output = json_output
        self.service_name = service_name

    def format(self, record):
        rec = logging.makeLogRecord(record.__dict__)
        try:
            rec.path = urlparse(request.url).path
            rec.trace_id = g.trace_id if 'trace_id' in g else ''
            rec.method = request.method
            rec.service_name = self.service_name
            rec.user_id = g.user_id if 'user_id' in g else request.headers.get("UID")
        except RuntimeError:
            rec.path = ''
            rec.trace_id = ''
            rec.method = ''
            rec.service_name = ''
            rec.user_id = ''
        return super().format(rec)


class JsonFormatter(RequestFormatter):
    """
    Setting the log output format conforms to the trace log specification
    """
    def __init__(self, service_name='Undefined'):
        log_format = {
            "log_create_time": "%(asctime)s",
            "traceid": "%(trace_id)s",
            "userid": "%(user_id)s",
            "level": "%(levelname)s",
            "service": "%(service_name)s",
            "method": "%(method)s",
            "process": "%(process)d",
            "path": "%(path)s",
            "message": "%(message)s"
        }
        time_format = '%Y-%m-%dT%H:%M:%S.000+00:00'
        super(JsonFormatter, self).__init__(
            json.dumps(log_format), time_format, False, service_name)

    def formatTime(self, record, datefmt=None):
        record_time = datetime.utcfromtimestamp(int(record.created))
        if datefmt:
            return record_time.strftime(datefmt)
        else:
            return record_time.isoformat()
