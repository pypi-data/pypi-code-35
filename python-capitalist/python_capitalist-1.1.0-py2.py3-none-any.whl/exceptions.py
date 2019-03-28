class CapitalistException(Exception):
    """Base exception for this library"""


class ImproperlyConfigured(CapitalistException):
    """Something is not provided in configuration"""

    def __init__(self, message=None):
        self.message = message


class RequestException(CapitalistException):
    """Indicate that there was an error with the incomplete HTTP request."""

    def __init__(self, original_exception, request_kwargs):
        """Initialize a RequestException instance.
        :param original_exception: The original exception that occurred.
        :param request_kwargs: The keyword arguments to the request function.
        """
        self.original_exception = original_exception
        self.request_kwargs = request_kwargs
        super(RequestException, self).__init__(
            "error with request {}".format(original_exception)
        )


class ResponseException(CapitalistException):
    """Indicate that there was an error with the completed HTTP request."""

    def __init__(self, code, message=None):
        """Initialize a ResponseException instance.
        :param code: Error code from Capitalist.
        :param message: Error message from Capitalist.
        """
        self.code = code
        self.message = message
        super(ResponseException, self).__init__(
            "received error with code {}".format(self.code)
        )
