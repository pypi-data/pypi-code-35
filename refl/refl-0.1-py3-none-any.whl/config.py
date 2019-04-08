#!/usr/bin/env python3

from os import path
from os.path import expanduser

HOME = expanduser("~")
ROOT = path.join(HOME, '.agdatool')

LOGGING = HOME
LOGFILE = 'agdatool.log'
LOGLEVEL = 'info'

