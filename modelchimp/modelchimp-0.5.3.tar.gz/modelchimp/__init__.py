import logging.config
import os

loggin_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging_config.ini')
logging.config.fileConfig(loggin_config_path)

from .tracker import Tracker
from .version import __version__
