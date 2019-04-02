#!/usr/bin/env python

import os
import urllib
from os.path import expanduser
import requests
import traceback
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta


# Specify files accessed by this script in guestshell
base_dir = expanduser('~') + '/cloud/authMgr/'
get_response_file = base_dir + "token_get_rsp"
debug_file = base_dir + "token_svr.log"
cert_file = "/etc/ssl/certs/ca-bundle.trust.crt"
token_file = base_dir + "token_file"


class AADAuth:

    def __doc__(self):
        """This class represents an application in Azure Active Directory"""

    def __init__(self, logger, cloud, tenant_id, app_id, app_key): #pragma: no cover
        self.logger = logger
        self.cloud = cloud
        self.app_id = app_id
        self.tenant_id = tenant_id
        self.token = ''
        self.token_expiry_time = datetime.utcnow() - timedelta(minutes=1)

        # Check if the app_key is URL encoded. If so, decode it
        if len(app_key) > 44 and app_key.count('%') > 0:
            self.app_key = urllib.unquote(app_key)
        else:
            self.app_key = app_key

        # Try to get a token
        token = self.get_token()
        if token == '':
            self.logger.error("AAD app failed verification: unable to obtain a token")

    def aad_get_token(self, cloud, tenant_id, app_id, app_key):
        if cloud == 'azure':
            url = "https://login.microsoftonline.com/%s/oauth2/token?api-version=1.1" % tenant_id
            payload = {'grant_type': 'client_credentials',
                       'client_id': app_id,
                       'resource': 'https://management.core.windows.net/',
                       'client_secret': app_key}

        elif cloud == 'azusgov':
            url = "https://login-us.microsoftonline.com/%s/oauth2/token?api-version=1.1" % tenant_id
            payload = {'grant_type': 'client_credentials',
                       'client_id': app_id,
                       'resource': 'https://management.core.usgovcloudapi.net/',
                       'client_secret': app_key}
        elif cloud == 'azchina':
            url = "https://login.chinacloudapi.cn/%s/oauth2/token?api-version=1.1" % tenant_id
            payload = {'grant_type': 'client_credentials',
                       'client_id': app_id,
                       'resource': 'https://management.core.chinacloudapi.cn/',
                       'client_secret': app_key}

        else:
            self.logger.error("Server: aad_get_token: invalid cloud name %s", cloud)
            return ''

        # Specify the HTTP POST request to obtain a token
        all_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Accept': 'accept:application/json',
                       'Authorization': 'OAuth 2.0'}

        # Send the HTTP POST request for the token
        try:
            response = requests.post(url, data=payload, verify=cert_file, headers=all_headers)
        except requests.exceptions.RequestException as e:
            self.logger.exception("Server: aad_get_token: request had error %s", str(e))
            return ''

        if 200 != response.status_code:
            self.logger.error("Server: aad_get_token: cloud: %s request failed rc=%d", cloud, response.status_code)
            with open(get_response_file, 'wb') as token_fh:
                for chunk in response.iter_content(chunk_size=64):
                    token_fh.write(chunk)
            return ''

        # Parse the HTTP GET response
        try:
            token = response.json()["access_token"]
            self.logger.info("Server: aad_get_token: cloud: {}, obtained token".format(cloud))

        except Exception as e:
            self.logger.exception("Server: aad_get_token:, cloud: %s caught exception %s", cloud, str(e))
            tb = traceback.format_exc()
            self.logger.exception("%s", tb)
            token = ''

        return token

    def get_token(self):
        if datetime.utcnow() < self.token_expiry_time:
            # Cached token is still valid. Just return it.
            return self.token
        else:
            # Need to refresh the token
            token = self.aad_get_token(self.cloud, self.tenant_id, self.app_id, self.app_key)
            if token != '':
                self.token = token
                self.token_expiry_time = datetime.utcnow() + timedelta(minutes=5)
                return self.token
            else:
                return ''

    def refresh_token(self):
        # Invalidate the current token
        self.token = ''
        self.token_expiry_time = datetime.utcnow() - timedelta(minutes=1)
        self.logger.info("Token successfully cleared")
        # Return a new token
        return self.get_token()

    def clear_token(self):
        self.token = ''
        self.token_expiry_time = datetime.utcnow()
        self.logger.info("Token successfully cleared")
        return 'OK'

    def show(self):
        buf = ''
        buf = buf + "\nApp ID:\t%s" % self.app_id
        buf = buf + "\nTenant ID:\t%s" % self.tenant_id
        buf = buf + "\nApp Key:\t%s" % self.app_key
        if self.token != '':
            buf = buf + "\nToken:\t%s" % self.token
            buf = buf + "\nExpires:\t%s" % self.token_expiry_time
            if self.token_expiry_time > datetime.utcnow():
                buf = buf + "\nToken is valid"
            else:
                buf = buf + "\nToken is expired"
        else:
            buf = buf + "\nNo token found"
        return buf
