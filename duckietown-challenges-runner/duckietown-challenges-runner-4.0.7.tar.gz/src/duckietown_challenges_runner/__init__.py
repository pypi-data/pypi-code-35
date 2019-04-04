# coding=utf-8
__version__ = '4.0.7'
import logging
import sys

logging.basicConfig()
dclogger = logging.getLogger('dt-challenges-runner')
dclogger.setLevel(logging.DEBUG)
dclogger.info('dt-challenges-runner %s' % __version__)
msg = f'Default encoding {sys.getdefaultencoding()}'
dclogger.debug(msg)
from .exceptions import *

from .runner import dt_challenges_evaluator

from .runner_local import runner_local_main
