"""Access Token Decorator

This decorator can be used to wrap any endpoint that needs to be protected.

"""

from brighthive_authlib.providers import OAuth2Provider


def token_required(provider: OAuth2Provider, scopes: list = []):
    def wrap(f):
        def wrapped_f(*args):
            if provider.validate_token(scopes=scopes):
                return f(*args)
        return wrapped_f
    return wrap
