# -*- coding: utf-8 -*-

import pickle

from contracts import describe_type
from . import logger
from .zc_debug_pickler import find_pickling_error
from .zc_safe_write import safe_read, safe_write

__all__ = [
    'safe_pickle_dump',
    'safe_pickle_load',
]

debug_pickling = False


def safe_pickle_dump(value, filename, protocol=pickle.HIGHEST_PROTOCOL,
                     **safe_write_options):
    with safe_write(filename, **safe_write_options) as f:
        try:
            pickle.dump(value, f, protocol)
        except KeyboardInterrupt:
            raise
        except BaseException:
            msg = 'Cannot pickle object of class %s' % describe_type(value)
            logger.error(msg)

            if debug_pickling:
                msg = find_pickling_error(value, protocol)
                logger.error(msg)
            raise


def safe_pickle_load(filename):
    # TODO: add debug check
    with safe_read(filename) as f:
        return pickle.load(f)
        # TODO: add pickling debug
