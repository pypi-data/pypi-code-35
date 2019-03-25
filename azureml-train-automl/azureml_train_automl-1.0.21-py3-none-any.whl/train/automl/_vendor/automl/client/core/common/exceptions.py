# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Exceptions thrown by AutoML."""


class ErrorTypes:
    """Possible types of errors."""

    User = 'User'
    Service = 'Service'
    Client = 'Client'
    Unclassified = 'Unclassified'
    All = {User, Service, Client, Unclassified}


class AutoMLException(Exception):
    """Exception with an additional field specifying what type of error it is."""

    def __init__(self, message="", error_type=ErrorTypes.Unclassified):
        """
        Construct a new AutoMLException.

        :param error_type: type of the exception.
        :param message: details on the exception.
        """
        super().__init__(message)
        self.error_type = error_type


class DataException(AutoMLException):
    """
    Exception related to data validations.

    :param message: Details on the exception.
    """

    def __init__(self, message=""):
        """
        Construct a new DataException.

        :param message: details on the exception.
        """
        super().__init__(message, ErrorTypes.User)


class ConfigException(AutoMLException):
    """
    Exception related to invalid user config.

    :param message: Details on the exception.
    """

    def __init__(self, message=""):
        """
        Construct a new ConfigException.

        :param message: details on the exception.
        """
        super().__init__(message, ErrorTypes.User)


class ServiceException(AutoMLException):
    """
    Exception related to JOS.

    :param message: Details on the exception.
    """

    def __init__(self, message=""):
        """
        Construct a new ServiceException.

        :param message: details on the exception.
        """
        super().__init__(message, ErrorTypes.Service)


class ClientException(AutoMLException):
    """
    Exception related to client.

    :param message: Details on the exception.
    """

    def __init__(self, message=""):
        """
        Construct a new ClientException.

        :param message: details on the exception.
        """
        super().__init__(message, ErrorTypes.Client)


class OnnxConvertException(ClientException):
    """Exception related to ONNX convert."""
