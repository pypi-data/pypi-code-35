"""Auth0 OAuth 2.0 Provider.

Implementation of an Auth0 OAuth 2.0 Provier.

"""

import requests
import json
from jose import jwt
from functools import wraps, partial
from flask import request
from brighthive_authlib.providers import OAuth2Provider, OAuth2ProviderError


class AuthZeroProvider(OAuth2Provider):
    """Auth0 OAuth 2.0 Provider."""

    def __init__(self):
        super().__init__()

    def validate_token(self, token=None, scopes=[]):
        if not token:
            token = self.get_token()

        try:
            headers = {'content-type': 'application/json'}
            jwks_keys = requests.get(self.jwks_url, headers=headers).json()
            unverified_header = jwt.get_unverified_header(token)

            rsa_key = {}
            for key in jwks_keys['keys']:
                if key['kid'] == unverified_header['kid']:
                    rsa_key = {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']
                    }
            if rsa_key:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=self.algorithms,
                    audience=self.audience,
                    issuer='{}/'.format(self.base_url))
                if len(scopes) == 0:
                    return True
                else:
                    unverified_claims = jwt.get_unverified_claims(token)
                    if unverified_claims.get('scope'):
                        token_scopes = unverified_claims['scope'].split()
                        for scope in scopes:
                            if scope not in token_scopes:
                                print(scope)
                                raise OAuth2ProviderError(
                                    'Required scope ({}) is not present for this client'.format(scope))
                    return True
        except Exception:
            raise OAuth2ProviderError('Access Denied')
