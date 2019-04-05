"""
:author: Gatsby Lee
:since: 2019-04-04
"""
import logging
import time

from functools import wraps

LOGGER = logging.getLogger(__name__)


def retry(exceptions_to_retry: tuple, max_retries: int,
          waittime_before_retrying: int):

    def deco_retry(func):
        @wraps(func)
        def func_retry(*args, **kwargs):
            retry_ct, waittime = max_retries, waittime_before_retrying
            while retry_ct > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions_to_retry as e:
                    LOGGER.info("[%s] %s, Retrying in %d seconds... (retry:%d|%d)",
                                type(e).__name__, e, waittime, retry_ct, max_retries)
                    time.sleep(waittime)
                    retry_ct -= 1
            return func(*args, **kwargs)

        return func_retry

    return deco_retry
