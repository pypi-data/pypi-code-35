#!/usr/bin/env python

import os
from os.path import expanduser
import requests
import subprocess
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
msi_dir = "/var/log/azure/Microsoft.ManagedIdentity.ManagedIdentityExtensionForLinux"
msi_service_file = "/etc/systemd/system/azuremsixtn.service"



class MSIAuth:

    def __doc__(self):
        """This class represents a Managed Service Identity (MSI) application in Azure Active Directory"""

    def __init__(self, logger): #pragma: no cover
        self.token = ''
        self.token_expiry_time = datetime.utcnow() - timedelta(minutes=1)
        self.logger = logger

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        # Try to get a token
        token = self.get_token()
        if token == '':
            self.logger.error("MSI app failed verification: unable to obtain a token")

    def msi_get_token_by_http(self):
        # Specify the HTTP GET request to obtain a token
        url = "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01"
        payload = {'resource': 'https://management.azure.com/'}
        header = {'Metadata': 'true'}

        # Send the HTTP GET request for the token
        try:
            response = requests.get(url, params=payload, verify=False, headers=header)
        except requests.exceptions.RequestException as e:
            self.logger.exception("Server: msi_get_token: request had an error %s", e)
            return ''

        if 200 != response.status_code:
            self.logger.error("Server: msi_get_token: request failed rc=%d", response.status_code)
            with open(token_file, 'wb') as token_fh:
                for chunk in response.iter_content(chunk_size=64):
                    token_fh.write(chunk)
            return ''

        # Parse the HTTP GET response
        try:
            token = response.json()["access_token"]
            self.logger.info("Server: msi_get_token: obtained token by HTTP")
        except Exception as e:
            self.logger.exception("Server: msi_get_token: caught exception %s", e)
            tb = traceback.format_exc()
            self.logger.exception("%s", tb)
            token = ''

        return token


    def msi_get_token_by_extension(self):
        # Check if user has successfully installed the Managed Identity Extension
        if not os.path.exists(msi_dir):
            # Directory does not exist.  Don't use MSI
            self.logger.info("Server: msi_get_token: MSI not installed")
            return ''

        # Check if the MSI service is running
        try:
            subprocess.check_output("pgrep -f msi-extension", shell=True)
        except:
            # Check if the Managed Identity Extension has been installed
            if os.path.exists(msi_service_file):
                # File has been installed.  Try to start the service.
                os.system("sudo systemctl enable azuremsixtn")
                os.system("sudo systemctl start azuremsixtn")
                self.logger.exception("Server: msi_get_token: started MSI service")
            else:
                # Directory does not exist.  Don't use MSI
                self.logger.exception("Server: msi_get_token: MSI not installed")
                return ''

        # Specify the HTTP GET request to obtain a token
        url = "http://localhost:50342/oauth2/token"
        payload = {'resource': 'https://management.azure.com/'}
        header = {'Metadata': 'true'}

        # Send the HTTP GET request for the token
        response = requests.get(url, params=payload, verify=False, headers=header)

        if 200 != response.status_code:
            self.logger.error("Server: msi_get_token: request failed rc=%d", response.status_code)
            with open(token_file, 'w') as token_fh:
                token_fh.write(response.json())
            return ''

        # Parse the HTTP GET response
        token = response.json()["access_token"]
        self.logger.info("Server: msi_get_token: obtained token by extension")

        return token

    def get_token(self):
        if datetime.utcnow() < self.token_expiry_time:
            # Cached token is still valid. Just return it.
            return self.token
        else:
            # Need to refresh the token
            token = self.msi_get_token_by_http()
            if token != '':
                self.token = token
                self.token_expiry_time = datetime.utcnow() + timedelta(minutes=5)
                return self.token
            else:
                # Try getting token by MSI extension
                token = self.msi_get_token_by_extension()
                if token != '':
                    self.token = token
                    self.token_expiry_time = datetime.utcnow() + timedelta(minutes=5)
                    return self.token
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
