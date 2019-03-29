"""Custom OAuth 2.0 Provider Error.

This class provides a custom OAuth 2.0 Provider Error.

"""


class OAuth2ProviderError(Exception):
    """Exception for OAuth2.0 Provider related problems.

    """

    def __init__(self, message):
        super().__init__(message)
