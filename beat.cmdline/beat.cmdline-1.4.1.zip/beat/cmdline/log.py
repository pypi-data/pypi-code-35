#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""Sets-up logging, centrally for beat cmdline
"""

import logging

def set_verbosity_level(logger, level):
    """Sets the log level for the given logger.

    Parameters
    ----------
    logger : :py:class:`logging.Logger` or str
        The logger to generate logs for, or the name  of the module to generate
        logs for.
    level : int
        Possible log levels are: 0: Error; 1: Warning; 2: Info; 3: Debug.
    Raises
    ------
    ValueError
        If the level is not in range(0, 4).
    """
    if level not in range(0, 4):
        raise ValueError(
            "The verbosity level %d does not exist. Please reduce the number "
            "of '--verbose' parameters in your command line" % level
        )
    # set up the verbosity level of the logging system
    log_level = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG
    }[level]

    # set this log level to the logger with the specified name
    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    logger.setLevel(log_level)
