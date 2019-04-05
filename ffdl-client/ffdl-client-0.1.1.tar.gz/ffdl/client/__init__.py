# -*- coding: utf-8 -*-

import requests

from requests.auth import HTTPBasicAuth


class Config:
    def __init__(self, api_endpoint=None, api_version='v1', version='2017-02-13', user=None, password=None, user_info=None):
        self._api_endpoint = api_endpoint
        self._api_version = api_version
        self._version = version
        self._user = user
        self._password = password
        self._user_info = user_info

    @property
    def api_endpoint(self):
        return self._api_endpoint

    @property
    def api_version(self):
        return self._api_version

    @property
    def version(self):
        return self._version

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._password

    @property
    def user_info(self):
        return self._user_info

    def is_valid(self):
        if not self._api_endpoint:
            raise ValueError('FfDL API endpoint is required')

        if not self._user:
            raise ValueError('FfDL user is required')

        if not self._user_info:
            raise ValueError('FfDL user info required')

        return True


class FfDLClient:
    def __init__(self, config:Config):
        """
        :param config: FfDL connection configuration
        """
        self.config = config

    def get(self, url):
        """
        Submit a get request to a FfDL server
        :param url: the api url path
        :return: a json payload with the api result
        """
        # validate that proper configuration has been provided
        self.config.is_valid()

        # accomodate provided strings starting with '/'
        if url.startswith('/'):
            url = url[1:]

        endpoint = self._create_ffdl_endpoint(url)

        headers = {'accept': 'application/json',
                   'X-Watson-Userinfo': self.config.user_info}

        try:
            result = requests.get(endpoint,
                                  auth=HTTPBasicAuth(self.config.user, self.config.password),
                                  headers=headers)

            return result.json()

        except requests.exceptions.Timeout:
            print("FFDL Job Submission Request Timed Out....")
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects were detected during job submission")
        except requests.exceptions.ConnectionError:
            print("Connection Error: Could not connect to {}".format(endpoint))
        except requests.exceptions.HTTPError as http_err:
            print("HTTP Error - {} ".format(http_err))
        except requests.exceptions.RequestException as err:
            print(err)

    def post(self, url, **file_paths):
        """
        Submit a post request to a FfDL server
        :param url: the api url path
        :param file_paths: files to submit with the post request
        :return: a json payload with the api result
        """
        # validate that proper configuration has been provided
        self.config.is_valid()

        # accomodate provided strings starting with '/'
        if url.startswith('/'):
            url = url[1:]

        endpoint = self._create_ffdl_endpoint(url)

        headers = {'accept': 'application/json',
                   'X-Watson-Userinfo': self.config.user_info}

        files = {}
        for name, path in file_paths.items():
            files[name] = open(file_paths[name], 'rb')

        try:
            result = requests.post(endpoint,
                                   auth=HTTPBasicAuth(self.config.user, self.config.password),
                                   headers=headers,
                                   files=files)

            return result.json()

        except requests.exceptions.Timeout:
            print("FfDL Job Submission Request Timed Out....")
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects were detected during job submission")
        except requests.exceptions.ConnectionError:
            print("Connection Error: Could not connect to {}".format(endpoint))
        except requests.exceptions.HTTPError as http_err:
            print("HTTP Error - {} ".format(http_err))
        except requests.exceptions.RequestException as err:
            print(err)

        finally:
            for name, file in files.items():
                file.close()

    def _create_ffdl_endpoint(self, url):
        """
        Utility method to create the FfDL api url based on FfDL
        server endpoint, api version and model version
        :param url:
        :return:
        """
        return "{}/{}/{}?version={}".format(self.config.api_endpoint, self.config.api_version, url, self.config.version)
