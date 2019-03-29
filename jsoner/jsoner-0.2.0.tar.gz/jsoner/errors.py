# -*- coding: utf-8 -*-


class JsonerException(Exception):
    """
    Base Exception class
    """
    pass


class JsonEncodingError(JsonerException):
    """
    This error occurs if *Jsoner* cannot encode your object to json.
    """
