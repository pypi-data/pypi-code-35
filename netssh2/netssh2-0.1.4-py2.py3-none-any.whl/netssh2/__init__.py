"""
Common code to be used in the whole netssh2 library
"""

from __future__ import unicode_literals, absolute_import
import logging

__version__ = "0.1.4"


def logger():
    """
    Set up logging
    :return: logging instance
    :rtype: class <logging.Logger>
    """
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    log = logging.getLogger(__name__)
    return log
