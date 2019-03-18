

class RealValidationError(Exception):
    """Base class for exceptions in this module."""
    pass


class InvalidTokenError(RealValidationError):
    """Raised when a token couldn't be enumerated. Tokens can passed as a
    parameter when initializing a ``RealValidation`` object or by setting the
    ``RV_TOKEN`` environmental variable before execution.

    """
    pass


class InvalidPhoneFormatError(RealValidationError):
    """Raised when a phone string doesn't match ``PHONE_REGEX``"""
    pass


class InvalidJSONResponseError(RealValidationError):
    """Raised when we couldn't decode a JSON response from a RealValidation
    API Request

    """
    pass


class ResponseCodeNotOkError(RealValidationError):
    """Raised when ``RESPONSECODE`` in a RealValidation JSON response does not
    equal ``OK``

    """
    pass


class MissingPhoneNumberError(ResponseCodeNotOkError):
    pass


class InvalidCustomerError(ResponseCodeNotOkError):
    pass


class InsufficientBalanceError(ResponseCodeNotOkError):
    pass


class InvalidPhoneError(ResponseCodeNotOkError):
    pass
