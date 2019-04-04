import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2LoginView,
    OAuth2CallbackView,
)
from .provider import iHelaProvider
from django.conf import settings


class iHelaAdapter(OAuth2Adapter):
    provider_id = iHelaProvider.id

    # Fetched programmatically, must be reachable from container
    access_token_url = "{}/oAuth2/token/".format(settings.OAUTH_SERVER_BASEURL)
    profile_url = "{}/api/connected-user/".format(settings.OAUTH_SERVER_BASEURL)

    # Accessed by the user browser, must be reachable by the host
    authorize_url = "{}/oAuth2/authorize/".format(settings.OAUTH_SERVER_BASEURL)

    # NOTE: trailing slashes in URLs are important, don't miss it

    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": "Bearer {0}".format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        # extra_data = {}
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(iHelaAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(iHelaAdapter)
