"""OAuth 2.0 Provider Base Class

This class is the base class for all OAuth 2.0 providers supported by the
libray.

"""

import os
import re
from flask import request
from brighthive_authlib.config import AuthLibConfiguration
from brighthive_authlib.providers import OAuth2ProviderError


class OAuth2Provider(object):
    """OAuth 2.0 Provider Base Class.

    Args:
        provider (str): Name of the OAuth 2.0 provider.
        base_url (str): Base URL for the OAuth 2.0 provider.
        jwks_url (str): URL for retrieving the application JSON Web Key Set.
        algorithms (list): Accepted JWT algorithms.
        audience (str): OAuth 2.0 audience parameter.

    """

    __slots__ = ['provider', 'base_url', 'jwks_url', 'algorithms', 'audience']

    def __init__(self):
        self.provider = None
        self.base_url = None
        self.jwks_url = None
        self.algorithms = None
        self.audience = None

    def from_object(self, obj: AuthLibConfiguration):
        """Configure the library from a configuration object.

        Args:
            obj (AuthLibConfiguration): A configuration object to pull configurations from.

        """

        self.provider = obj.provider
        self.base_url = obj.base_url
        self.jwks_url = obj.jwks_url
        self.algorithms = obj.algorithms
        self.audience = obj.audience

    def from_env(self):
        """Configure the library from the OS environemt."""

        self.provider = os.getenv('OAUTH2_PROVIDER', None)
        self.base_url = os.getenv('OAUTH2_BASE_URL', None)
        self.jwks_url = os.getenv('OAUTH2_JWKS_URL', None)
        self.algorithms = os.getenv('OAUTH2_ALGORITHMS', None)
        self.audience = os.getenv('OAUTH2_AUDIENCE', None)

    def get_token(self):
        """Retrieve the token from the Flask request header.

        Returns:
            str: The auth token extracted from the authorization header.

        Raises:
            OAuth2ProviderError: If the Authorization header is invalid.

        """

        auth_token = request.headers.get('Authorization', None)
        if not auth_token:
            raise OAuth2ProviderError('No authorization header provided.')

        auth_token = re.split('\\s+', auth_token)
        if str(auth_token[0]).upper() != 'BEARER':
            raise OAuth2ProviderError('Authorization must be a bearer token.')

        if len(auth_token) != 2:
            raise OAuth2ProviderError('Invalid token provided.')

        return auth_token[1]

    def validate_token(self, token: str, scopes: list = []):
        """Validate the access token provided by the client.

        Args:
            token (str): OAuth 2.0 bearer token to validate.

            grants (list): List of OAuth 2.0 grants to validate against.

        Returns:
            bool: True if the client is authorized to access the resource, False otherwise.

        """
        pass
