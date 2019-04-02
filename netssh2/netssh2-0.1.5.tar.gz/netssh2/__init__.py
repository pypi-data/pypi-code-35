"""
Common code to be used in the whole netssh2 library
"""

from __future__ import unicode_literals, absolute_import
import logging

__version__ = "0.1.5"
__FORMAT = '%(asctime)s - %(message)s'
__DATEFORMAT = '%d-%b-%y %H:%M:%S'
__LOGGER_NAME = "netssh2_main_logger"


logging.basicConfig(level=logging.WARN, format=__FORMAT, datefmt=__DATEFORMAT)
# I like the name "log" even though it should be in uppercase, let's mute pylint on this
log = logging.getLogger(__LOGGER_NAME)  # pylint: disable=C0103


def set_logging_level(new_level):
    """
    Sets logging level to new desired level.
    :param new_level: name of logging level
    :type new_level: string
    :return: True
    :rtype: bool
    """
    logging.getLogger(__LOGGER_NAME).setLevel(logging.getLevelName(new_level.upper()))
    return True
