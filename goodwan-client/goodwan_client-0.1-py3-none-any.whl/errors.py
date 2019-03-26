"""
GoodWan client library: errors
"""


class ApiError(Exception):
    """ Basic error class """


class ParameterError(ApiError):
    """ Parameter error """


class CommunicationError(ApiError):
    """ Communication error """


class ProtocolError(ApiError):
    """ Protocol error """


class ParseError(ProtocolError):
    """ Parse error """
