import inspect
from datetime import datetime
from functools import wraps

from sidecar.cloud_logger.file_logger import ICloudLogger
from sidecar.cloud_logger.logs import ServiceLogEntry, ServiceLogEntryLogType


class ServiceLogger:
    file_logger = None  # type: ICloudLogger
    ignored = []

    @staticmethod
    def wrap(cls):
        for (attr_name, attr_value) in cls.__dict__.items():
            if inspect.isroutine(attr_value) and \
                    not attr_name.startswith('__') and \
                    not isinstance(attr_value, staticmethod) and \
                    not isinstance(attr_value, classmethod) and \
                    attr_name not in ServiceLogger.ignored:
                setattr(cls, attr_name, ServiceLogger.wrapper(func=attr_value))
        return cls

    @staticmethod
    def ignore(func):
        ServiceLogger.ignored.append(func.__name__)
        return func

    @staticmethod
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            service = kwargs["name"]
            func_name = func.__qualname__
            ServiceLogger.file_logger.write(ServiceLogEntry(name=service,
                                                            log_events=[(datetime.utcnow(),
                                                                         "{} start".format(func_name))],
                                                            log_type=ServiceLogEntryLogType.LOG))
            func(*args, **kwargs)
            ServiceLogger.file_logger.write(ServiceLogEntry(name=service,
                                                            log_events=[(datetime.utcnow(),
                                                                         "{} end".format(func_name))],
                                                            log_type=ServiceLogEntryLogType.LOG))

        return wrapped

    @classmethod
    def set_logger(cls, file_logger):
        cls.file_logger = file_logger
