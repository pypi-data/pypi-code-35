"""
Logging configuration module
"""
import logging
import os
import tempfile
from logging.config import dictConfig
from pathlib import Path


class Logging:
    def __init__(self, log_level_global=None, log_level_file=None,
                 log_level_console=None, results_dir=None, **kwargs):
        self._log_level_global = log_level_global or os.getenv('KTDK_LOG_LEVEL', 'INFO')
        self._log_level_file = log_level_file or os.getenv('KTDK_LOG_LEVEL_FILE',
                                                           self._log_level_global)
        self._log_level_console = log_level_console or os.getenv('KTDK_LOG_LEVEL_CONSOLE',
                                                                 self._log_level_global)
        self._results_dir = results_dir

    @property
    def log_level_global(self) -> str:
        return self._log_level_global

    @property
    def log_level_file(self) -> str:
        return self._log_level_file

    @property
    def log_level_console(self) -> str:
        return self._log_level_console

    @property
    def handlers(self):
        return {
            'console': self.get_handler_console(),
            'results_file': self.get_logger_file('results'),
        }

    @property
    def formatters(self):
        return {
            'verbose': {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'},
            'simple': {'format': '%(levelname)s %(message)s'},
            'colored_console': {
                '()': 'coloredlogs.ColoredFormatter',
                'format': "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                'datefmt': '%H:%M:%S'
            },
        }

    @property
    def loggers(self) -> dict:
        return {
            'ktdk': {
                'handlers': ['console', 'results_file'],
                'level': self.log_level_global, 'propagate': True
            },
            'tests': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': True},
        }

    @property
    def logger_config(self):
        return {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': self.formatters,
            'handlers': self.handlers,
            'loggers': self.loggers,
        }

    @property
    def results_dir(self) -> Path:
        results = self._results_dir or tempfile.gettempdir()
        return Path(results)

    def get_logger_file(self, name, level: str = None):
        level = level or self.log_level_file
        results_dir = self.results_dir
        if not results_dir.exists():
            results_dir.mkdir(parents=True)
        return {
            'level': level,
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': str(self.results_dir / f'{name}.log'),
            'maxBytes': 5000000,  # 5MB
            'backupCount': 5
        }

    def get_handler_console(self, level: str = None):
        level = level or self.log_level_console
        return {
            'level': level, 'class': 'logging.StreamHandler', 'formatter': 'colored_console'
        }

    def load_config(self):
        """Loads config based on the config type
        Args:
        """
        add_custom_log_level()
        dictConfig(self.logger_config)
        reenable_loggers()


TRACE_LOG_LVL = 9


def _trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LOG_LVL):
        # Yes, logger takes its '*args' as 'args'.
        self._log(TRACE_LOG_LVL, message, args, **kws)


def add_custom_log_level():
    logging.addLevelName(TRACE_LOG_LVL, 'TRACE')
    logging.Logger.trace = _trace


def load_config(**config):
    return Logging(**config).load_config()


def reenable_loggers():
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.disabled = False
