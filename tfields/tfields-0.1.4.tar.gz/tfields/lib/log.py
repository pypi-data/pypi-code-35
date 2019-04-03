from contextlib import contextmanager
import logging
import time


def progressbar(iterable, log=None):
    """
    Examples:
        >>> import logging
        >>> import tfields
        >>> import sys
        >>> sys.modules['tqdm'] = None
        >>> log = logging.getLogger(__name__)

        >>> a = range(3)
        >>> for value in tfields.lib.log.progressbar(a, log=log):
        ...     _ = value * 3
    
    """
    if log is None:
        log = logging.getLogger()
    try:
        from tqdm import tqdm as progressor
        tqdm_exists = True
    except ImportError as err:
        def progressor(iterable):
            """
            dummy function. Doe nothing
            """
            return iterable
        tqdm_exists = False
    try:
        nTotal = len(iterable)
    except:
        nTotal = None

    for i in progressor(iterable):
        if not tqdm_exists:
            if nTotal is None:
                log.info("Progress: item {i}".format(**locals()))
            else:
                log.info("Progress: {i} / {nTotal}".format(**locals()))
        yield i


@contextmanager
def timeit(msg="No Description", log=None, precision=1):
    """
    Context manager for autmated timeing
    Args:
        msg (str): message to customize the log message
        log (logger)
        precision (int): show until 10^-<precision> digits
    """
    if log is None:
        log = logging.getLogger()
    startTime = time.time()
    log.log(logging.INFO, "-> " * 30)
    message = "Starting Process: {0} ->".format(msg)
    log.log(logging.INFO, message)

    yield

    log.log(logging.INFO, "\t\t\t\t\t\t<- Process Duration:"
            "{value:1.{precision}f} s".format(value=time.time() - startTime,
                                              precision=precision))
    log.log(logging.INFO, "<- " * 30)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
