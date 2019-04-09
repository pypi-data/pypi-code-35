# coding: utf-8
import hues
import os
import platform
import re
from collections import namedtuple
from dophon import properties
from logging import Formatter

# Unicorns
from hues.huestr import HueString as huestr
from hues.console import Config, SimpleConsole, PowerlineConsole

p_sys_type = platform.system()
as_tuples = lambda name, obj: namedtuple(name, obj.keys())(**obj)

DEBUG = 0
WARNING = 1
INFO = 2
SUCCESS = 3
ERROR = 4

logging_config = properties.logger_config \
    if hasattr(properties, 'logger_config') and properties.logger_config \
    else \
    {
        # 'filename': 'app.log',
        # 'level': 'logging.DEBUG',
        'format': '%(levelname)s : (%(asctime)s) ==> ::: %(message)s',
        # 'format': '%(levelname)s %(name)s: <%(module)s> (%(asctime)s) ==> %(filename)s {%(funcName)s} [line:%(lineno)d] ::: %(message)s',
        'time_format': '%Y-%m-%d %H:%M:%S',
        'show_time': 'yes',
        'add_newline': 'yes',
        'theme': 'simple'
    }

# 默认等级为INFO
LOG_LEVEL = eval(logging_config['level'].upper()) if 'level' in logging_config else INFO

conf = Config()

setattr(conf, 'opts', as_tuples('Options', logging_config))

console = SimpleConsole(conf=conf)


# 日志过滤非框架打印
class DefFilter:
    """
    默认过滤器
    """

    def filter(self, record):
        return eval(record['level'].upper()) >= LOG_LEVEL and record.name.startswith('dophon') and record.levelno >= \
               logging_config['level']


class DefFormatter:
    """
    默认格式管理器
    """

    def __init__(self, fmt_rule: str = logging_config):
        self._fmt_rule = fmt_rule

    def format(self, message: object):
        return self._fmt_rule % message if isinstance(message, tuple) else str(message)


class DophonLogger:
    _filter = DefFilter()
    _formatter = DefFormatter()

    def __init__(self, *args, **kwargs):
        self.logger = console
        # hues.SimpleConsole.conf = conf
        # for name in dir(conf.opts):
        #     print(f'{name} ==> {getattr(conf.opts,name)}')

    def __getattr__(self, item):
        if callable(item):
            print('callable !')
        else:
            pass

    def debug(self, message: object):
        self._debug(LOG_LEVEL, self._formatter.format(message))

    def warning(self, message: object):
        self._warning(LOG_LEVEL, self._formatter.format(message))

    def warn(self, message: object):
        self._warning(LOG_LEVEL, self._formatter.format(message))

    def info(self, message: object):
        self._info(LOG_LEVEL, self._formatter.format(message))

    def success(self, message: object):
        self._success(LOG_LEVEL, self._formatter.format(message))

    def error(self, message: object):
        self._error(LOG_LEVEL, self._formatter.format(message))

    def log(self, message: object):
        self.logger.log(self._formatter.format(message))

    def _debug(self, level: str, message: object):
        self.logger.debug(str(message))

    def _warning(self, level: str, message: object):
        self.logger.warn(str(message))

    def _info(self, level: str, message: object):
        self.logger.info(str(message))

    def _success(self, level: str, message: object):
        self.logger.success(str(message))

    def _error(self, level: str, message: object):
        self.logger.error(str(message))

    def addFilter(self, filter):
        self._filter = filter


def inject_logger(g: dict, var_name: str = 'logger'):
    # logger = logging.getLogger('dophon.' + re.sub('\..*', '', g['__file__'].split(os.path.sep)[-1]))
    logger = DophonLogger('dophon.' + re.sub('\..*', '', g['__file__'].split(os.path.sep)[-1]))
    # logger.addFilter(DefFilter())
    g[var_name] = logger
