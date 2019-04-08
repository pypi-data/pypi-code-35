#!/usr/bin/env python3

import sys, os

import coloredlogs, logging
from logging.handlers import RotatingFileHandler
from typing import *

from .config import *


def logger(logPath:str=LOGGING, fileName:str=LOGFILE, level:str='DEBUG'):

    logFormatter:Any = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger:Any = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, level.upper()))

    return logger


class Logging:
  def __init__(self:Any, level:str='info'):
    self.logger = logger(level)

    coloredlogs.install(level='DEBUG', logger=self.logger)
    coloredlogs.install(level='INFO', logger=self.logger)
    coloredlogs.install(level='WARNING', logger=self.logger)
    coloredlogs.install(level='ERROR', logger=self.logger)
    coloredlogs.install(level='CRITICAL', logger=self.logger)

  def __call__(self:Any):
    return self.logger
