import os
import sys
import logging
from logging.handlers import RotatingFileHandler

class MaxLevelFilter:
    def __init__(self, maxLevel):
        self.maxLevel = maxLevel
    def filter(self, logRecord):
        return logRecord.levelno <= self.maxLevel

def setupLogger():
    logFormatter = logging.Formatter('[%(levelname)s:%(asctime)s][SDC] %(message)s', '%Y-%m-%dT%H:%M:%S')
    logFolder = os.getenv('APP_LOG_PATH', None)
    logger = logging.getLogger('samtecdeviceshare')
    logger.setLevel(logging.INFO)
    if logFolder:
        infoFileHandler = RotatingFileHandler(
            filename=os.path.join(logFolder, 'samtecdeviceshare.info.log'),
            maxBytes=3*1024*1024,
            backupCount=10
        )
        infoFileHandler.setFormatter(logFormatter)
        infoFileHandler.setLevel(logging.INFO)
        infoFileHandler.addFilter(MaxLevelFilter(logging.WARNING))
        logger.addHandler(infoFileHandler)

        errorFileHandler = RotatingFileHandler(
            filename=os.path.join(logFolder, 'samtecdeviceshare.error.log'),
            maxBytes=3*1024*1024,
            backupCount=10
        )
        errorFileHandler.setFormatter(logFormatter)
        errorFileHandler.setLevel(logging.ERROR)
        logger.addHandler(errorFileHandler)

    if os.getenv('PYTHON_ENV') == 'development' or logFolder is None:
        soHandler = logging.StreamHandler(sys.stdout)
        soHandler.setFormatter(logFormatter)
        soHandler.setLevel(logging.INFO)
        seHandler = logging.StreamHandler(sys.stderr)
        seHandler.setFormatter(logFormatter)
        seHandler.setLevel(logging.ERROR)
        logger.addHandler(soHandler)
        logger.addHandler(seHandler)
    return logger
