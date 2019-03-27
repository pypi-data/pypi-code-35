# -*- coding: utf-8 -*-

"""
IP2LOC Config File
"""

import logging
import os


_CURRENT_PATH = os.path.split(os.path.realpath(__file__))[0]

# ------ LOGGING ------
LOG_LEVEL = logging.DEBUG
LOG_FILE_PATH = os.path.join(_CURRENT_PATH, 'data/logs')
LOG_FORMAT = '%(levelname)s (%(asctime)s) %(filename)s > %(funcName)s > line %(lineno)d: \n\t%(message)s'

# ------ PATH ------
RAW_CSV_PATH_NAME = os.path.join(_CURRENT_PATH, 'data/IP2LOCATION-LITE-DB5.CSV')
RAW_ZIP_PATH_NAME = os.path.join(_CURRENT_PATH, 'data/IP2LOCATION-LITE-DB5.CSV.ZIP')
SQLITE_DATA_PATH_NAME = os.path.join(_CURRENT_PATH, 'data/data.db')

# ------ Server ------
PORTS = (8080, )
