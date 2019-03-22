"""Unit Tests for Provider Factory."""

import pytest
from expects import expect, be, raise_error, be_a, be_none, equal
from brighthive_authlib import OAuth2ProviderError, OAuth2ProviderFactory, AuthZeroProvider, AuthLibConfiguration


class TestProviderFactory(object):
    """Provider Factory Test Class."""

    def test_create_bad_oauth_provider(self):
        """Test that the factory raises an OAuth2ProviderError when an invalid OAuth 2.0 provider is requested."""
        with pytest.raises(OAuth2ProviderError):
            expect(OAuth2ProviderFactory.get_provider(
                'i_am_an_unknown_provider')).to(raise_error(OAuth2ProviderError))

    def test_create_auth0_provider(self):
        """Test the ability to create an Auth0 provider."""

        # no configuration
        provider = OAuth2ProviderFactory.get_provider('auth0')
        expect(provider).to(be_a(AuthZeroProvider))
        expect(provider.base_url).to(be_none)
        expect(provider.algorithms).to(be_none)

        # bad configuration
        bad_config_obj = object()
        with pytest.raises(OAuth2ProviderError):
            expect(OAuth2ProviderFactory.get_provider(
                'auth0', bad_config_obj)).to(raise_error)

        # legitimate configuration
        config_obj = AuthLibConfiguration(provider='AUTH0', base_url='http://localhost:8000',
                                          jwks_url='http://path/to/jwks', algorithms=['foo'], audience='audience-01')
        provider = OAuth2ProviderFactory.get_provider(
            'auth0', config=config_obj)
        expect(provider.provider).to(equal(config_obj.provider))
        expect(provider.base_url).to(equal(config_obj.base_url))
        expect(provider.jwks_url).to(equal(config_obj.jwks_url))
        expect(provider.algorithms).to(equal(config_obj.algorithms))
        expect(provider.audience).to(equal(config_obj.audience))
