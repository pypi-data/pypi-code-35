# coding:utf-8
from __future__ import absolute_import, unicode_literals, print_function

import time

import json
import logging
import six
import socket
import traceback


class JSONFormatter(logging.Formatter):
    def __init__(self):
        self.hostname = socket.gethostname()

    def format_exception(self, exc_info):
        return ''.join(traceback.format_exception(*exc_info))

    def format(self, record, **extra):
        data = {
            'host': self.hostname,
            'message': record.getMessage(),
            'path': record.pathname,
            'lineno': record.lineno,
            'level': record.levelname,
            'logger_name': record.name,
            'exc_info': '',
            # 'thread_name': record.threadName,
            # 'thread': record.thread,
            # 'process_name': record.processName,
            # 'process': record.process,
            'created': record.created or time.time(),
        }

        if record.exc_info:
            data.update({'exc_info': self.format_exception(record.exc_info)})

        data.update(extra)

        for key in data:
            if not isinstance(data[key], six.string_types) and key != 'created':
                data[key] = six.text_type(data[key])
        return self.serialize(data)

    def serialize(self, data):
        if six.PY2:
            return json.dumps(data)
        else:
            return bytes(json.dumps(data), 'utf-8')
