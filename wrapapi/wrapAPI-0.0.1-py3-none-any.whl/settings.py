
import os

from wrapapi.logger import request_logging


class Settings(object):

    log_level = 'INFO'
    logger = request_logging
    headers = os.getenv('HEADERS') or {'Content-Type': 'Application/json'}
    cookie = os.getenv('COOKIE') or {}
    timeout = os.getenv('TIMEOUT') or 20
    verify = os.getenv('VERIFY') or False

    base_url = None
