#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import getpass
import keyring
import EtnaAPI


class GetpassAuthenticator:
    """
    Regular interactive authenticator for CLI-based apps
    """

    def authenticate(self, session, retry=False):
        """
        Attempt to authenticate

        :param session:             the session to authenticate
        :param retry:               True if the authentication should be retried until successful, False otherwise

        :return:                    the authenticated session

        :raises EtnaAPI.AuthError:  if the authentication failed and :param retry: is False
        """
        while True:
            try:
                user = input("Login: ")
                passwd = getpass.getpass()
                session.authenticate(user, passwd)
                return session
            except EtnaAPI.AuthError as ex:
                if not retry:
                    raise ex


class KeyringAuthenticator:
    """
    Keyring-based authenticator

    On OSX, OSX Keychain will be used
    On Linux, Gnome Keyring will be used
    """

    @staticmethod
    def __get_git_email():
        return subprocess.check_output(["git", "config", "--get", "user.email"]).decode("utf-8")

    def authenticate(self, session):
        """
        Attempt to authenticate
        If a saved password cannot be found in the keyring, one will asked.
        If the authentication then succeeds with the newly-provided password, the latter will be saved

        :param session:             the session to authenticate

        :return:                    the authenticated session
        """
        user = self.__get_git_email().split('@')[0]
        passwd = keyring.get_password("auth.etna-alternance.net", user)
        while True:
            if not passwd:
                passwd = getpass.getpass()
                keyring.set_password("auth.etna-alternance.net", user, passwd)
            try:
                session.authenticate(user, passwd)
                return session
            except EtnaAPI.AuthError:
                print("Authentication failed")
                keyring.delete_password("auth.etna-alternance.net", user)
                passwd = None
