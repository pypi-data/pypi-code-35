"""An OAuth 2.0 Provider Factory.

This class implements an OAuth 2.0 factory that is responsible for creating new
providers on demand.

"""

from brighthive_authlib.config import AuthLibConfiguration
from brighthive_authlib.providers import AuthZeroProvider, OAuth2ProviderError


class OAuth2ProviderFactory(object):
    """OAuth 2.0 Provider Factory.

    Methods:
        get_provider (OAuth2Provider):
            Returns an OAuth2.0 provider.

    """

    @staticmethod
    def get_provider(provider: str = 'AUTH0', config: AuthLibConfiguration = None):
        """Returns an OAuth 2.0 Provder.

        Params:
            provider (str):
                The name of the provider (default is AUTH0)
            config (AuthLibConfiguration):
                The configuration object to pass to the newly created provider.

        """

        if str(provider).upper() == 'AUTH0':
            provider = AuthZeroProvider()
        else:
            raise OAuth2ProviderError(
                'Unknown OAuth 2.0 Provider: {}'.format(str(provider).upper()))

        if config is not None:
            try:
                provider.from_object(config)
            except AttributeError:
                raise OAuth2ProviderError(
                    'Unable to configure library with the provided configuration')

        return provider
