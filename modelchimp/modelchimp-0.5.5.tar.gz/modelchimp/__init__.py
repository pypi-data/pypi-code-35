import logging.config
from os import path
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging_config.ini')
logging.config.fileConfig(log_file_path)

from .tracker import Tracker
from .version import __version__
