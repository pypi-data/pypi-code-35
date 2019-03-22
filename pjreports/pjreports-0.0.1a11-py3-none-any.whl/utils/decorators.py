__author__ = "Martín Ezequiel Collado, HRL-UPM"

import logging
import os

import time
from raven import Client
from raven.conf import setup_logging
from raven.handlers.logging import SentryHandler


def create_logger(name: str, level: str, config_box):
    """
    Creates a logging object and returns it
    :param name: str. Name for the logger.
    :param level: str. Setup the logger level.
    :return logger: logger. Return the logger object

    :Info:
    Levels: [ CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET ]

    :Example:
        logger_test_debug = create_logger('testing-logger', 'DEBUG')

        @logger(logger_test_debug)
        def wrong_func():
            1 / 0

    """
    logger_level = level.lower()

    logger = logging.getLogger(name)
    levels_available = dict(critical=logging.CRITICAL, error=logging.ERROR, warning=logging.WARNING, info=logging.INFO,
                            debug=logging.DEBUG, notset=logging.NOTSET)

    try:
        logger.setLevel(levels_available.get(logger_level))

        if config_box.LOGGER.SENTRY_ENABLE:
            client = Client(config_box.LOGGER.SENTRY_URL)
            handler = SentryHandler(client)
            handler.setLevel(levels_available.get(logger_level))
            setup_logging(handler)

        # create the logging file handler
        fhdirectory = os.path.join(config_box.DIRECTORIES.LOGS, name)
        fh = logging.FileHandler(fhdirectory)

        fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)
        fh.setFormatter(formatter)

        # add handler to logger object
        logger.addHandler(fh)
        return logger
    except:
        raise Exception('Set a proper logger level. '
                        'Loggers level available: [ CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET]')




def logger(logger_handler):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    :param logger_handler: The logging object
    """

    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the logger
                err = "There was a logger in  "
                err += func.__name__
                logger_handler.exception(err)

                # re-raise the logger
                raise

        return wrapper

    return decorator


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed
