# coding:utf-8
from __future__ import absolute_import, unicode_literals, print_function

import sys
from datetime import datetime, timedelta

import atexit
import logging
import six
import traceback
import kafka
from kafka.errors import KafkaTimeoutError
from logging.handlers import SocketHandler

from .formatters import JSONFormatter


class LogstashHandler(SocketHandler):
    def __init__(self, host, port, formatter=None):
        super(LogstashHandler, self).__init__(host, port)
        self.formatter = formatter or JSONFormatter()

    def makePickle(self, record):
        return self.formatter.format(record) + b"\n"


def get_topic_prefix(default=None):
    try:
        from flask import current_app
        return current_app.config['SERVER_ENVIRONMENT']
    except (Exception, RuntimeError):
        pass

    try:
        # noinspection PyUnresolvedReferences
        from settings import SERVER_ENVIRONMENT
        return SERVER_ENVIRONMENT
    except ImportError:
        pass
    return default


# noinspection PyTypeChecker
class KafkaHandler(logging.Handler):
    def __init__(self, bootstrap_servers, level=logging.NOTSET, formatter=None,
                 **kwargs):
        logging.Handler.__init__(self, level)
        self.immediate_flush = kwargs.get('immediate_flush', False)
        self.flush_timeout = kwargs.get('flush_timeout', 5)
        self.formatter = formatter or JSONFormatter()
        self.bootstrap_servers = bootstrap_servers
        self._producer = None
        self.max_block_ms = kwargs.get('max_block_ms', 150)

        self._connect_retry_after_seconds = kwargs.get(
            'connect_retry_after_seconds', 30
        )
        self._last_connect_try = datetime.utcnow() - timedelta(
            seconds=self._connect_retry_after_seconds
        )

    def get_producer(self):
        if self._producer:
            return self._producer
        td = timedelta(seconds=self._connect_retry_after_seconds)
        if datetime.utcnow() - self._last_connect_try < td:
            return
        else:
            self._last_connect_try = datetime.utcnow()

        self._producer = kafka.KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            max_block_ms=self.max_block_ms,
        )

        return self._producer

    def flush(self):
        try:
            if self._producer:
                self._producer.flush(timeout=self.flush_timeout)
        except KafkaTimeoutError:
            self.console_error(
                "Unable to flush records within timeout=%ss\n" % (
                    self.flush_timeout
                ), sys.exc_info())

    def emit(self, record):
        extra = self.get_extra()
        if all([
            extra.get('request_id', '???') == '???',
            extra.get('task_name', '???') == '???',
            extra.get('task_id', '???') == '???',
        ]):
            return

        if record.name == 'kafka':
            return
        try:
            prefix = get_topic_prefix()
            suffix = 'logline'
            topic = '_'.join(filter(bool, [prefix, suffix]))
            payload = self.formatter.format(record, **extra)
            producer = self.get_producer()
            if producer:
                producer.send(topic, payload)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        if self._producer:
            self._producer.close(timeout=self.flush_timeout)
        logging.Handler.close(self)

    def console_error(self, message, exc_info=None):
        if sys.stderr:
            try:
                if exc_info:
                    traceback.print_exception(
                        etype=exc_info[0],
                        value=exc_info[1],
                        tb=exc_info[2],
                        file=sys.stderr,
                    )
                sys.stderr.write(message)
            except IOError:
                pass
            finally:
                del exc_info

    def get_extra(self):
        extra = {}

        try:
            from flask import request
            extra['request_id'] = request.headers.get('X-Request-Id', '???')
        except:
            extra['request_id'] = '???'

        try:
            from celery._state import get_current_task
            task = get_current_task()
            extra['task_name'] = six.text_type(task.name)
            extra['task_id'] = six.text_type(task.request.id)
        except:
            extra['task_name'] = '???'
            extra['task_id'] = '???'

        if all([
            extra['request_id'] == '???',
            extra['task_id'] != '???' and extra['task_name'] != '???',
        ]):
            try:
                extra['request_id'] = ":".join([
                    extra['task_name'],
                    extra['task_id'],
                ])
            except:
                pass
        return extra


@atexit.register
def flush_logs_at_exit():
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if isinstance(handler, KafkaHandler):
            handler.flush()
