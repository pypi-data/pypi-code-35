#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class EtnaAPIError(Exception):
    """
    Generic error
    """
    def __init__(self, msg):
        super().__init__(msg)


class AuthError(EtnaAPIError):
    """
    Authentication error, raised when an authentication attempt fails
    """
    def __init__(self, msg):
        super().__init__(msg)


class AccessDenied(EtnaAPIError):
    """
    Access denied error, raised when a request fails because the user has insufficient rights
    """
    def __init__(self, msg):
        super().__init__(msg)


class BadRequest(EtnaAPIError):
    """
    Bad request error, raised when a request is ill-formed (incorrect body, incorrect activity type, etc)
    """
    def __init__(self, msg):
        super().__init__(msg)


class NotFound(EtnaAPIError):
    """
    Not found error, raised when a resource cannot be found
    """
    def __init__(self, msg):
        super().__init__(msg)
