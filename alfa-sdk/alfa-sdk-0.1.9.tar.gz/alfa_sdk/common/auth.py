import os
import requests

from alfa_sdk.common.helpers import EndpointHelper
from alfa_sdk.common.stores import AuthStore
from alfa_sdk.common.exceptions import (
    CredentialsError,
    TokenNotFoundError,
    AuthenticationError,
)


ALFA_APP_ID = 30


class Authentication:
    user = None
    access_token = None
    auth0_token = None

    def __init__(self, credentials={}, *, alfa_env):
        endpoint = EndpointHelper(alfa_env=alfa_env)
        url_core = endpoint.resolve("core")
        self._authenticate(url_core, credentials)

    def _authenticate(self, url_core, credentials):
        try:
            access_token, auth0_token = fetch_tokens(credentials)
            self.user = validate_token(url_core, access_token, auth0_token)
            self.access_token = access_token
            self.auth0_token = auth0_token
        except:
            client_id, client_secret = fetch_credentials(credentials)
            auth0_token = request_auth0_token(url_core, client_id, client_secret)
            self.user = validate_token(url_core, None, auth0_token)
            self.auth0_token = auth0_token

    def get_token(self):
        if self.access_token:
            return self.access_token, "access_token"
        if self.auth0_token:
            return self.auth0_token, "auth0_token"
        raise TokenNotFoundError()

    def authenticate_request(self, options):
        return authenticate_request(options, self.access_token, self.auth0_token)


#


def fetch_tokens(credentials={}):
    store = AuthStore.get_group()
    cache = AuthStore.get_group("cache")

    if "access_token" not in credentials:
        if "ALFA_ACCESS_TOKEN" in os.environ:
            credentials["access_token"] = os.environ.get("ALFA_ACCESS_TOKEN")
        elif store and "access_token" in store:
            credentials["access_token"] = store["access_token"]
        elif cache and "access_token" in cache:
            credentials["access_token"] = cache["access_token"]

    if "auth0_token" not in credentials:
        if "ALFA_AUTH0_TOKEN" in os.environ:
            credentials["auth0_token"] = os.environ.get("ALFA_AUTH0_TOKEN")
        elif store and "auth0_token" in store:
            credentials["auth0_token"] = store["auth0_token"]
        elif cache and "auth0_token" in cache:
            credentials["auth0_token"] = cache["auth0_token"]

    if "access_token" not in credentials and "auth0_token" not in credentials:
        raise TokenNotFoundError()

    return credentials.get("access_token"), credentials.get("auth0_token")


def fetch_credentials(credentials={}):
    if "client_id" not in credentials:
        store = AuthStore.get_group()

        if "ALFA_CLIENT_ID" in os.environ:
            credentials["client_id"] = os.environ.get("ALFA_CLIENT_ID")
        elif store and "client_id" in store:
            credentials["client_id"] = store["client_id"]

        if "ALFA_CLIENT_SECRET" in os.environ:
            credentials["client_secret"] = os.environ.get("ALFA_CLIENT_SECRET")
        elif store and "client_secret" in store:
            credentials["client_secret"] = store["client_secret"]

    if "client_id" not in credentials or "client_secret" not in credentials:
        raise CredentialsError()

    return credentials.get("client_id"), credentials.get("client_secret")


#


def request_auth0_token(url_core, client_id, client_secret):
    url = url_core + "/api/ApiKeyValidators/requestToken"

    res = requests.post(
        url,
        data={
            "clientId": client_id,
            "clientSecret": client_secret,
            "audience": url_core,
        },
    )
    res = res.json()

    if "error" in res:
        raise AuthenticationError(error=str(res.get("error")))

    token = res["token_type"] + " " + res["access_token"]
    return token


def validate_token(url_core, access_token, auth0_token=None):
    if access_token:
        url = url_core + "/api/WbUsers/getRole"
    elif auth0_token:
        url = url_core + "/api/ApiKeyValidators/validateTokenForApp"
    else:
        raise AuthenticationError(error="No tokens were supplied")

    options = {"params": {"appId": ALFA_APP_ID}}
    options = authenticate_request(options, access_token, auth0_token)
    res = requests.get(url, **options)
    res = res.json()

    if "error" in res:
        raise AuthenticationError(error=str(res.get("error")))

    return res


def authenticate_request(options, access_token, auth0_token=None):
    if not access_token and not auth0_token:
        raise TokenNotFoundError()

    if "params" not in options:
        options["params"] = {}
    if "headers" not in options:
        options["headers"] = {}

    if access_token:
        options["headers"]["access_token"] = access_token
        options["params"]["access_token"] = access_token
    if auth0_token:
        options["headers"]["wb-authorization"] = auth0_token

    return options

