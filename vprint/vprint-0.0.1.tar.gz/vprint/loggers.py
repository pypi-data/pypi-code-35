import logging
import sys

from vprint.vprint_level import get_vprint_level
from vprint.formatting import PathTruncatingFormatter


def get_verbose_logger(name='verbose_logger', verbose=False,
                       max_name_len=20,
                       fmt='%(filename)s:%(lineno)d> %(message)s',
                       datefmt='%d-%m-%Y:%H:%M:%S'):
    """
    Initialize a basic stream logger to be used instead of the fallback logger
    Like Instant Logger, but only prints when VPRINTV (or verbose) is set
    Args:
        name: logger name
        verbose: If true, ignore the env variable and generate a logger
            which always prints
        fmt: formatting string. see logging.Formatter
        datefmt: date format string. see logging.Formatter

    Returns:
        logger object
    """
    if get_vprint_level() > 0 or verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = 0

    vp_log_format = PathTruncatingFormatter(
        fmt=fmt, datefmt=datefmt,
        max_name_len=max_name_len
    )

    # todo: add existing logger check
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(loglevel)
    console_handler.setFormatter(vp_log_format)
    logger.addHandler(console_handler)
    # Shut off hierarchical logging propagation to prevent dupes
    logger.propagate = False
    return logger
