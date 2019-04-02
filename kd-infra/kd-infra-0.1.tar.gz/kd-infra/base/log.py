# -*- coding:utf-8 -*-
import logging
import time
import sys
import os



initialized = False
formatter = logging.Formatter('%(asctime)s %(levelname)s %(process)d [%(filename)s:%(lineno)d %(funcName)s]: %(message)s')

log_level = 'info'
log_dir_common = '/home/hadoop/logs_jaguar/common.txt'
log_dir_web_service = '/home/hadoop/logs_jaguar/web_service.txt'
log_dir_monitor = '/home/hadoop/logs_jaguar/monitor.txt'
log_dir_heart_beat = '/home/hadoop/logs_jaguar/heart_beat.txt'
log_dir_task_trigger = '/home/hadoop/logs_jaguar/task_trigger.txt'
log_dir_controller = '/home/hadoop/logs_jaguar/controller.txt'
log_dir_status = '/home/hadoop/logs_jaguar/status.txt'
log_dir_status_pipe = '/home/hadoop/logs_jaguar/status_pipe.txt'
log_dir_job_collector = '/home/hadoop/logs_jaguar/job_collector.txt'
log_dir_scheduler = '/home/hadoop/logs_jaguar/scheduler.txt'
log_dir_trigger = '/home/hadoop/logs_jaguar/trigger.txt'

class Configer():
    def __init__(self):
        self.__log_path = ""
        self.__file_handler = None
        self.__console_handler = None
        self.__pure_path = log_dir_common
        self.__time_format = "%Y%m%d%H%M"
        self.__time_format = "%Y%m%d"

    inst = None

    @staticmethod
    def get():
        if Configer.inst == None:
            Configer.inst = Configer()
        return Configer.inst

    def set_file_handler(self):
        date_str = time.strftime(self.__time_format)
        self.__log_path = self.__pure_path + '.' + date_str

        fh = logging.FileHandler(self.__log_path)
        fh.setFormatter(formatter)
        self.__file_handler = fh
        logging.getLogger('').addHandler(fh)

    def set_console_handler(self):
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        self.__console_handler = console
        logging.getLogger('').addHandler(console)
        logging.getLogger('').setLevel(logging.INFO)

    def del_console_handler(self):
        logging.getLogger('').removeHandler(self.__console_handler)
        del self.__console_handler
        self.__console_handler = None

    def del_file_handler(self):
        logging.getLogger('').removeHandler(self.__file_handler)
        del self.__file_handler
        self.__file_handler = None

    def rotate(self):
        date_str = time.strftime(self.__time_format)
        path = self.__pure_path + '.' + date_str
        self.__log_path

        if path == self.__log_path:
            return
        sys.stdout.flush()
        sys.stderr.flush()
        self.del_file_handler()
        self.set_file_handler()

    def init(self, level, path=log_dir_common, quiet=False):
        self.__pure_path = path
        if quiet:
            self.del_console_handler()

        if not quiet and not self.__console_handler:
            self.set_console_handler()
        self.set_file_handler()

        cmd = str("logging.getLogger("").setLevel(logging.%s)" % (level.upper()))
        exec cmd


class Logger():
    def __init__(self):
        self.info = logging.info
        self.debug = logging.debug
        self.warning = logging.warning
        self.error = logging.error
        self.critical = logging.critical
        Configer.get().set_console_handler()


def log_init(level, path=log_dir_common, quiet=True):
    global initialized
    if initialized: return
    Configer.get().init(level, path, quiet)
    initialized = True


g_logger = Logger()


def logger():
    Configer.get().rotate()
    return g_logger

def log(log_name):
    def decorator(func):
        def wrapper(*args, **kw):
            quiet = False
            if log_name == 'heart_beat':
                quiet = True
            if log_name == 'status_pipe':
                quiet = True
            log_init(log_level, 'log_dir_' + log_name,
                     quiet = quiet)
            return func(*args, **kw)
        return wrapper
    return decorator

if __name__ == '__main__':
    log_init('info', './log.txt', quiet=False)

    while True:
        l = logger()
        l.info('abc')
        time.sleep(1)
