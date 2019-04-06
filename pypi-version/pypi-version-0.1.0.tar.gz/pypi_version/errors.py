"""
Provide implementation of the error for PyPi version checking.
"""
NOT_SUPPORTED_CONTINUOUS_INTEGRATION_ERROR_MESSAGE = 'Continuous integration `{ci_name}` is not supported.'


class NotSupportedContinuousIntegrationError(Exception):
    """
    Not supported continuous integration error.
    """

    def __init__(self, message):
        self.message = message
