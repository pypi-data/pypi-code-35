import logging

from .constants import LOG_FORMAT, LOG_LEVEL

file_handler = logging.FileHandler('./realvalidation.log')
stream_handler = logging.StreamHandler()

handlers = [file_handler, stream_handler]

logging.basicConfig(level=LOG_LEVEL,
                    format=LOG_FORMAT,
                    handlers=handlers)
