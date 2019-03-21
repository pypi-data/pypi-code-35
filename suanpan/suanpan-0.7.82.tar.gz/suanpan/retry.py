# coding=utf-8
from __future__ import print_function

import functools
import traceback

import retrying

from suanpan.log import logger


def _log(func):
    @functools.wraps(func)
    def _dec(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.warning("Run failed and retrying: {}".format(func.__name__))
            logger.warning(traceback.format_exc())
            raise e

    return _dec


def retry(*args, **kwargs):
    def _wrap(func):
        kwargs.update(wrap_exception=True)
        _retry = retrying.retry(*args, **kwargs)
        _func = _retry(_log(func))

        @functools.wraps(func)
        def _dec(*fargs, **fkwargs):
            try:
                return _func(*fargs, **fkwargs)
            except retrying.RetryError as e:
                logger.error(
                    "Retry failed after {} attempts: {}".format(
                        e.last_attempt.attempt_number, func.__name__
                    )
                )
                raise e

        return _dec

    return _wrap
