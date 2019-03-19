# -*- coding: utf-8 -*-
import os
import json
import time
import logging
import datetime
import functools
from aws_lambda_sls import KinesisService
from kombu.utils.objects import cached_property

logger = logging.getLogger(__name__)
DEFAULT_PARTITION_KEY = "simu.models.monitor.MonitorData"
DEFAULT_STREAM_NAME = "tianfu_redshift_kinesis_stream"


def format_data(data_list):
    def _convert(data):
        if isinstance(data, dict):
            for key, value in data.items():
                data[key] = _convert(value)
        elif isinstance(data, list):
            for idx, value in enumerate(data):
                data[idx] = _convert(value)
        elif isinstance(data, datetime.datetime):
            data = datetime.datetime.strftime(data, "%Y-%m-%d %H:%M:%S")
        return data
    return _convert(data_list)


class MonitorService(object):
    def __init__(self, server_name=None, project_name=None, docker_name=None,
                 aws_params=None, partition_key=None, debug=False, debug_handle=None,
                 stream_name=None):
        self.server_name = server_name
        self.project_name = project_name
        self.docker_name = docker_name
        self.aws_params = aws_params
        self.debug = debug
        self.partition_key = partition_key or DEFAULT_PARTITION_KEY
        self.debug_handle = debug_handle
        self.stream_name = stream_name or DEFAULT_STREAM_NAME
        self.load_env()
    
    def load_env(self):
        try:
            if not os.path.exists("/etc/monitor.conf"):
                return
            config = json.load(open("/etc/monitor.conf"))
            if "server_name" in config:
                self.server_name = config["server_name"]
            if "project_name" in config:
                self.project_name = config["project_name"]
            if "docker_name" in config:
                self.docker_name = config["docker_name"]
            if "partition_key" in config:
                self.partition_key = config["partition_key"]
            if "stream_name" in config:
                self.stream_name = config["stream_name"]
        except Exception as ex:
            logger.error(str(ex))

    @cached_property
    def kins_analytics(self):
        return KinesisService(self.stream_name, aws_params=self.aws_params)

    def push_task(self, tn, ty="worker", tr=0, ts=1, t_start=None,
                  t_end=None, remark="正常", t_params=None):
        data = format_data(dict(
            ms=self.server_name,
            mp=self.project_name,
            md=self.docker_name,
            tn=tn,
            ty=ty,
            tr=tr,
            ts=ts,
            t_start=t_start or datetime.datetime.now(),
            t_end=t_end or datetime.datetime.now(),
            remark=remark, t_params=t_params
        ))
        if self.debug:
            if self.debug_handle:
                self.debug_handle(data)
        else:
            self.kins_analytics.push_record(data, self.partition_key)
            logger.info("#push kinesis: %s", json.dumps(data))

    def monitor_task(self, name=None, ty="celery"):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*sub, **kw):
                t_params = "(%s,%s)" % (sub, kw)
                tr, t_start, t_end = 0, None, None
                try:
                    a, t_start = time.time(), datetime.datetime.now()
                    ret = func(*sub, **kw)
                    b, t_end = time.time(), datetime.datetime.now()
                    tr = int((b - a) * 1000)
                    tn = "%s.%s" % (func.__module__, name or func.__name__)
                    self.push_task(tn, ty=ty, tr=tr, t_start=t_start,
                                   t_end=t_end, t_params=t_params)
                    return ret
                except Exception as ex:
                    self.push_task(func.__name__, ty=ty, tr=tr, ts=0, t_start=t_start,
                                   t_end=t_end, remark=str(ex), t_params=t_params)
                    raise ex
            return wrapper
        return decorator
