"""
Module for defining netssh2 exceptions
"""
from __future__ import absolute_import
from ssh2.exceptions import Timeout, AuthenticationError  # pylint: disable=E0611


class NetSsh2AuthenticationError(AuthenticationError):  # pylint: disable=R0903
    """
    Base exception for any authentication errors
    """


class NetSsh2Timeout(Timeout):  # pylint: disable=R0903
    """
    Base exception for any timeout errors
    """


class NetSsh2ChannelException(Exception):
    """
    Base exception for any channel errors
    """


class NetSsh2TooManyRetriesException(Exception):
    """
    Base exception when ran out of retries.
    """


class NetSsh2HostError(Exception):
    """
    Base exception for any host errors
    """
