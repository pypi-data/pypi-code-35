# -*- coding: utf-8 -*-
"""
Handler Module
--------------

Contains the peer handler and should have nothing else.
"""

__all__ = [
    'THREAD_LIMIT',
    'PORT_RANGE',
    'PORT_START',
    'LOGGER',
    'DEV',
    'GROUP',
    'IS_HUB',
    'HOST_IP'
]

# std imports
import os
import socket
from logging import getLogger, StreamHandler, Formatter, DEBUG

# thread limit
THREAD_LIMIT = int(os.environ.setdefault("NET_THREAD_LIMIT", "5"))

# networking
HOST_IP = socket.gethostbyname(socket.gethostname())
PORT_START = int(os.environ.setdefault("NET_PORT", "3010"))
PORT_RANGE = int(os.environ.setdefault("NET_PORT_RANGE", "5"))

# peer configuration
GROUP = str(os.environ.get("NET_GROUP"))
IS_HUB = os.environ.get("NET_IS_HUB") is not None


# handle development environment
DEV = os.environ.get("NET_DEV")

# configure logger
LOGGER = getLogger('net')

LOGGER_HANDLER = StreamHandler()
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER_HANDLER.setFormatter(Formatter("%(name)s:%(levelname)s\t%(message)s"))

if DEV:
    LOGGER.setLevel(DEBUG)
