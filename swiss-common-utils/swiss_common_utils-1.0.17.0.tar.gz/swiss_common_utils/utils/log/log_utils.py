import logging
import time

import coloredlogs
import pyfiglet

logger = None


def get_logger(level='DEBUG', filename=None):
    global logger
    if logger:
        return logger

    logging.basicConfig(format='%(asctime)s %(funcName)s():%(lineno)i:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename=filename)
    logger = logging.getLogger()
    coloredlogs.install(level=level)
    return logger


def log_enter_and_exit(orig_func):
    logger = get_logger()

    def wrapper(*args, **kwargs):
        func_full_name = '.'.join([orig_func.__module__, orig_func.__qualname__])
        logger.debug('[ENTER] {}'.format(func_full_name))
        start = int(time.time()) * 1000
        result = orig_func(*args, **kwargs)
        run_time = (int(time.time()) * 1000) - start
        logger.debug('[EXIT] {} (Execution time: {}ms)'.format(func_full_name, run_time))
        return result

    return wrapper


def log_function_args_and_kwargs(orig_func):
    logger = get_logger()

    def wrapper(*args, **kwargs):
        logger.info('Function: {} run with args: {}, and kwargs: {}'.format(orig_func.__name__, args, kwargs))
        return orig_func(*args, **kwargs)

    return wrapper


def log_function_runtime_in_ms(orig_func):
    logger = get_logger()
    import time

    def wrapper(*args, **kwargs):
        start = int(time.time()) * 1000
        result = orig_func(*args, **kwargs)
        run_time = (int(time.time()) * 1000) - start
        logger.info('Function: {} ran time: {}ms'.format(orig_func.__name__, run_time))
        return result

    return wrapper


def print_ascii_art(text, font=pyfiglet.DEFAULT_FONT):
    print()
    print(pyfiglet.figlet_format(text=text, font=font))
    print()
