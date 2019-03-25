import logging.config
logging.config.fileConfig('modelchimp/logging_config.ini')

from .tracker import Tracker
from .version import __version__
