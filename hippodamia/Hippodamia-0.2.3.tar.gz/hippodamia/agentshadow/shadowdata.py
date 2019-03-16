import datetime
from pelops.mylogger import get_log_level
from logging import NOTSET
import collections
import threading


class ShadowLogging:
    class Entry:
        log = None
        counter = None
        time = None

        def __init__(self, maxlen):
            self.log = collections.deque(maxlen=maxlen)
            self.counter = 0

        def add(self, message):
            self.log.appendleft(message)
            self.counter += 1
            self.time = datetime.datetime.now()

        def stats(self):
            output = "received: {}, stored: {}, @{}".format(self.counter, len(self.log), self.time)
            return output

    flat_list = None
    level_dict = None
    max_level = None
    set_health = None

    def __init__(self, maxlen=50, set_health=None):
        self.set_health = set_health
        self.reset_max_level()
        self.flat_list = ShadowLogging.Entry(maxlen)
        self.level_dict = collections.defaultdict(lambda: ShadowLogging.Entry(maxlen))

    def add(self, message):
        self.flat_list.add(message)
        level = get_log_level(message["level"])
        self.level_dict[level].add(message)
        self.max_level = max(self.max_level, level)
        self.set_health(self.max_level)

    def reset_max_level(self):
        self.max_level = NOTSET
        self.set_health(self.max_level)


class ShadowData:
    gid = None

    properties = None
    properties_time = None

    request = {}
    request_counter = 0
    request_time = None

    config = {}
    config_counter = 0
    config_time = None

    runtime = {}
    runtime_counter = 0
    runtime_time = None

    ping = {}
    ping_counter = 0
    ping_time = None

    end = {}
    end_counter = 0
    end_time = None

    logger = None

    def __init__(self, gid, set_log_health):
        self.gid = str(gid)
        self.logger = ShadowLogging(50, set_log_health)

    def process_properties(self, properties):
        self.properties = properties.export_dict()
        self.properties_time = datetime.datetime.now()

    def process_ping(self, message):
        self.ping = message
        self.ping_counter += 1
        self.ping_time = datetime.datetime.now()

    def process_config(self, message):
        self.config = message
        self.config_counter += 1
        self.config_time = datetime.datetime.now()

    def process_runtime(self, message):
        self.runtime = message
        self.runtime_counter += 1
        self.runtime_time = datetime.datetime.now()

    def process_end(self, message):
        self.end = message
        self.end_counter += 1
        self.end_time = datetime.datetime.now()

    def process_logger(self, message):
        self.logger.add(message)

    def _get_logger_time(self):
        return self.logger.flat_list.time

    logger_time = property(fget=_get_logger_time)

    def _get_logger_counter(self):
        return self.logger.flat_list.counter

    logger_counter = property(fget=_get_logger_counter)

    def process_request(self, message):
        self.request = message
        self.request_counter += 1
        self.request_time = datetime.datetime.now()

    def get_counter_dict(self):
        result = {
            "request": self.request_counter,
            "ping": self.ping_counter,
            "runtime": self.runtime_counter,
            "config": self.config_counter,
            "logger": self.logger_counter,
            "end": self.end_counter
        }
        return result

    def get_stats(self):
        return "request {}, ping {}, runtime {}, config {}, logger {}, end {}"\
            .format(self.request_counter, self.ping_counter, self.runtime_counter,
                    self.config_counter, self.logger_counter, self.end_counter)
