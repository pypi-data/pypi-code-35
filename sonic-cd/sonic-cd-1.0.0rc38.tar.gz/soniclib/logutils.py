import logging
import threading
import os
import re

from soniclib.context import Context


class LogStashFilter(logging.Filter):
    __seq = 0

    def __init__(self, level=logging.INFO):
        super(LogStashFilter, self).__init__()
        self.context = Context()
        self.container_regex = re.compile("\A(\w+)\s+\|")
        self.log_level = level

    def filter(self, record):
        self.__seq += 1
        record.logSequence = self.__seq
        record.pipe_id = self.context.get("pipe_id")
        record.task_id = self.context.get("task_id")
        record.loggerName = "sonic"
        if record.levelname:
            record.loglevel = record.levelname
        if record.msg and type(record.msg) == str:
            # suppress compose progress unless started with --debug
            if not self.log_level == logging.DEBUG and "Creating" in record.msg:
                return False
            match = self.container_regex.match(record.msg)
            if match:
                record.container = match.group(1)
        return True


class LogPipe(threading.Thread):

    def __init__(self, level):
        threading.Thread.__init__(self)
        self.daemon = False
        self.level = level
        self.fdRead, self.fdWrite = os.pipe()
        self.pipeReader = os.fdopen(self.fdRead)
        self.logger = logging.getLogger()
        self.logger.addFilter(LogStashFilter(level))
        self.start()

    def fileno(self):
        return self.fdWrite

    def run(self):
        for line in iter(self.pipeReader.readline, ''):
            self.logger.log(self.level, line.strip('\n'))

        self.pipeReader.close()

    def close(self):
        os.close(self.fdWrite)

    def __exit__(self, type, value, traceback):
        self.close()

    def __enter__(self):
        return self
