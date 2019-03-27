import logging
import sys
import traceback

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = 0

# Stream Handler
formatter = logging.Formatter('[%(levelname)s]%(module)s:%(lineno)d'
                              '{%(funcName)s}:%(message)s')

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

# File Handler

file_handler = logging.FileHandler('/logs/textos.log')

formatter = logging.Formatter('{"@timestamp":"%(asctime)s",'
                              '"@version":1,'
                              '"message": "%(message)s",'
                              '"logger_name": "%(module)s",'
                              '"thread_name": "%(threadName)s",'
                              '"level": "%(levelname)s",'
                              '"level_value": "%(levelno)s",'
                              '"stack_trace": "' +
                              traceback.format_exc().strip() + '",'
                              '"app_name": "textos"}')

file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
