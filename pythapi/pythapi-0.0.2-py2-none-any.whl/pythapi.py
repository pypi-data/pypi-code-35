import requests
import json
import sys
import time
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+
from random import choice

class Connect():

    authorization = "Basic token"

    def __init__(self, node_ip, base_url):
        self.host = node_ip
        self.url = base_url
    
    def _authorization_header(self):
        authorization_header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self.authorization
        }
        return authorization_header

    def _header(self):
        header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        return header

    def _common_api(self, call_type, api_endpoint, config=None, authentication=True):

        # Determine if authentication should be sent as part of the API Header
        if authentication:
            header = self._authorization_header()
        elif authentication is False:
            header = self._header()
        else:
            sys.exit('Error: "authentication" must be either True or False')

        try:
            if call_type == 'GET':
                request_url = "https://{}{}{}".format(
                    self.host, self.url, api_endpoint)
                request_url = quote(request_url, '://?=&')
                api_request = requests.get(
                    request_url, verify=False, headers=header)
            elif call_type == 'POST':
                config = json.dumps(config)
                request_url = "https://{}{}{}".format(
                    self.host, self.url, api_endpoint)
                api_request = requests.post(
                        request_url,
                        verify=False,
                        headers=header,
                        data=config)
            elif call_type == 'PUT':
                config = json.dumps(config)
                print(config)
                request_url = "https://{}{}{}".format(
                    self.host, self.url, api_endpoint)
                api_request = requests.put(request_url, verify=False, headers=header, data=config)
            elif call_type == 'DELETE':
                request_url = "https://{}{}{}".format(
                    self.host, self.url, api_endpoint)
                api_request = requests.delete(
                    request_url, verify=False, headers=header)
            else:
                sys.exit('Error: the _common_api() call_type must be one of the following: {}'.format(
                    ['GET', 'POST', 'PUT', 'DELETE']))
        except requests.exceptions.ConnectTimeout:
            sys.exit(
                "Error: Unable to establish a connection to the endpoint.")
        except requests.exceptions.ReadTimeout:
            sys.exit("Error: The endpoint did not respond to the API request in the allotted amount of time.")
        except requests.exceptions.RequestException as error:
            # If "error_message" has be defined sys.exit that message else
            # sys.exit the request exception error
            try:
                error_message
            except NameError:
                sys.exit(error)
            else:
                sys.exit('Error: ' + error_message)
        else:
            try:
                return api_request.json()
            except BaseException:
                return {'status_code': api_request.status_code}

    def get(self, api_endpoint, authentication=True):
        return self._common_api(
            'GET',
            api_endpoint,
            authentication=authentication)

    def post(self, api_endpoint, config, authentication=True):
        return self._common_api(
            'POST',
            api_endpoint,
            config=config,
            authentication=authentication)

    def put(self, api_endpoint, config, authentication=True):
        return self._common_api(
            'PUT',
            api_endpoint,
            config=config,
            authentication=authentication)

    def delete(self, api_endpoint, authentication=True):
        return self._common_api(
            'DELETE',
            api_endpoint,
            authentication=authentication)