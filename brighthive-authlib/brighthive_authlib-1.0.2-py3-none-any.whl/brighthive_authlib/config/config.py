"""Application configuration.

"""


class AuthLibConfiguration(object):
    """Configuration class.

    This class encapsulates all the necessary information needed by
    an OAuth 2.0 provider in order to validate a token.

    Args:
        provider (str): Name of the OAuth 2.0 provider.
        base_url (str): Base URL for the OAuth 2.0 provider.
        jwks_url (str): URL for retrieving the application JSON Web Key Set.
        algorithms (list): Accepted JWT algorithms.
        audience (str): OAuth 2.0 audience parameter.

    """

    def __init__(self, provider: str = None, base_url: str = None,
                 jwks_url: str = None, algorithms: list = None,
                 audience: str = None):
        self.provider = provider
        self.base_url = base_url
        self.jwks_url = jwks_url
        self.algorithms = algorithms
        self.audience = audience
