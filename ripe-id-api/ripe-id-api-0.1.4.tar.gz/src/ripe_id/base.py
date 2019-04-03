#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from . import token
from . import account

RIPEID_BASE_URL = "https://id.platforme.com/api/"
""" The default base URL to be used when no other
base URL value is provided to the constructor """

RIPEID_LOGIN_URL = "https://id.platforme.com/"
""" The default login URL to be used when no other
base URL value is provided to the constructor """

SCOPE = (
    "account.me",
    "account.acl"
)
""" The list of permissions to be used to create the
scope string for the oauth value """

class API(
    appier.OAuth2API,
    token.TokenAPI,
    account.AccountAPI
):

    def __init__(self, *args, **kwargs):
        appier.OAuth2API.__init__(self, *args, **kwargs)
        self.base_url = appier.conf("RIPEID_BASE_URL", RIPEID_BASE_URL)
        self.login_url = appier.conf("RIPEID_LOGIN_URL", RIPEID_LOGIN_URL)
        self.client_id = appier.conf("RIPEID_ID", None)
        self.client_secret = appier.conf("RIPEID_SECRET", None)
        self.redirect_url = appier.conf("RIPEID_REDIRECT_URL", None)
        self.base_url = kwargs.get("base_url", self.base_url)
        self.login_url = kwargs.get("login_url", self.login_url)
        self.client_id = kwargs.get("client_id", self.client_id)
        self.client_secret = kwargs.get("client_secret", self.client_secret)
        self.redirect_url = kwargs.get("redirect_url", self.redirect_url)
        self.scope = kwargs.get("scope", SCOPE)
        self.access_token = kwargs.get("access_token", None)
        self.refresh_token = kwargs.get("refresh_token", None)
        self.session_id = kwargs.get("session_id", None)

    def build(
        self,
        method,
        url,
        data = None,
        data_j = None,
        data_m = None,
        headers = None,
        params = None,
        mime = None,
        kwargs = None
    ):
        appier.OAuth2API.build(
            self,
            method,
            url,
            data = data,
            data_j = data_j,
            data_m = data_m,
            headers = headers,
            params = params,
            mime = mime,
            kwargs = kwargs
        )
        auth = kwargs.pop("auth", True)
        if auth: params["sid"] = self.get_session_id()

    def get_session_id(self):
        if self.session_id: return self.session_id
        return self.oauth_login()

    def auth_callback(self, params, headers):
        if self.refresh_token:
            self.oauth_refresh()
            params["access_token"] = self.get_access_token()
        if self.session_id:
            self.session_id = None
            session_id = self.get_session_id()
            params["sid"] = session_id

    def oauth_authorize(self, state = None):
        url = self.login_url + "oauth2/auth"
        appier.verify_many((
            self.client_id,
            self.redirect_url,
            self.scope
        ))
        values = dict(
            client_id = self.client_id,
            redirect_uri = self.redirect_url,
            response_type = "code",
            scope = " ".join(self.scope)
        )
        if state: values["state"] = state
        data = appier.legacy.urlencode(values)
        url = url + "?" + data
        return url

    def oauth_access(self, code):
        url = self.login_url + "oauth2/token"
        contents = self.post(
            url,
            token = False,
            auth = False,
            client_id = self.client_id,
            client_secret = self.client_secret,
            grant_type = "authorization_code",
            redirect_uri = self.redirect_url,
            code = code
        )
        self.access_token = contents["access_token"]
        self.refresh_token = contents.get("refresh_token", None)
        self.trigger("access_token", self.access_token)
        self.trigger("refresh_token", self.refresh_token)
        return self.access_token

    def oauth_refresh(self):
        url = self.login_url + "oauth2/token"
        contents = self.post(
            url,
            callback = False,
            token = False,
            auth = False,
            client_id = self.client_id,
            client_secret = self.client_secret,
            grant_type = "refresh_token",
            redirect_uri = self.redirect_url,
            refresh_token = self.refresh_token
        )
        self.access_token = contents["access_token"]
        self.trigger("access_token", self.access_token)
        return self.access_token

    def oauth_login(self):
        url = self.login_url + "oauth2/login"
        contents = self.post(url, callback = False, token = True, auth = False)
        self.session_id = contents.get("session_id", None)
        self.tokens = contents.get("tokens", None)
        self.trigger("auth", contents)
        return self.session_id

    @property
    def oauth_types(self):
        return ("param",)

    @property
    def token_default(self):
        return False
