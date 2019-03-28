"""
SkylabGenesis - Python Client
For more information, visit https://genesis.skylabtech.ai
"""

import json
import logging
import requests

from .version import VERSION

API_HEADER_KEY = 'X-SLT-API-KEY'
API_HEADER_CLIENT = 'X-SLT-API-CLIENT'

LOGGER = logging.getLogger('skylab_genesis')
LOGGER.propagate = False

class api: #pylint: disable=invalid-name
    """
    The client for accessing the Skylab Genesis platform.

    Args:
        api_key (str): Your account's API KEY.

    Attributes:
        api_proto (str): The API endpoint protocol.
        api_port (str): The API endpoint port.
        api_host (str): The API endpoint host name.
        api_version (str): The API endpoint version number.
        api_key (str): The API key to use.
        debug (boolean): Whether or not to allow debugging information to be printed.
    """

    api_proto = 'https'
    api_port = '443'
    api_host = 'genesis.skylabtech.ai'
    api_version = '1'
    api_key = 'THIS_IS_A_TEST_API_KEY'

    debug = False

    def __init__(self, api_key=None, **kwargs):
        if not api_key:
            raise Exception("You must specify an api key")

        self.api_key = api_key

        if 'api_host' in kwargs:
            self.api_host = kwargs['api_host']
        if 'api_proto' in kwargs:
            self.api_proto = kwargs['api_proto']
        if 'api_port' in kwargs:
            self.api_port = kwargs['api_port']
        if 'api_version' in kwargs:
            self.api_version = kwargs['api_version']
        if 'debug' in kwargs:
            self.debug = kwargs['debug']

        if self.debug:
            logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.DEBUG)

            LOGGER.debug('Debug enabled')
            LOGGER.propagate = True

    def _build_http_auth(self):
        return (self.api_key, '')

    @staticmethod
    def _build_request_headers():
        client_header = '%s-%s' % (
            'python',
            VERSION
        )

        headers = {
            API_HEADER_CLIENT: client_header,
            'Content-type': 'application/json',
            'Accept': 'text/plain'
        }

        return headers

    def _build_request_path(self, endpoint):
        path = '/api/v%s/%s' % (self.api_version, endpoint)

        path = "%s://%s:%s%s" % (
            self.api_proto,
            self.api_host,
            self.api_port,
            path
        )

        return path

    @staticmethod
    def _build_payload(data):
        if not data:
            return None

        return json.dumps(data)

    def _api_request(self, endpoint, http_method, **kwargs):
        """Private method for api requests"""
        LOGGER.debug(' > Sending API request to endpoint: %s', endpoint)

        auth = self._build_http_auth()

        headers = self._build_request_headers()
        LOGGER.debug('\theaders: %s', headers)

        path = self._build_request_path(endpoint)
        LOGGER.debug('\tpath: %s', path)

        data = self._build_payload(kwargs.get('payload'))
        if not data:
            data = kwargs.get('data')
        LOGGER.debug('\tdata: %s', data)

        req_kw = dict(
            auth=auth,
            headers=headers,
        )

        if http_method == 'POST':
            if data:
                response = requests.post(path, data=data, **req_kw)
            else:
                response = requests.post(path, **req_kw)
        elif http_method == 'PUT':
            response = requests.put(path, data=data, **req_kw)
        elif http_method == 'DELETE':
            response = requests.delete(path, **req_kw)
        else:
            response = requests.get(path, **req_kw)

        LOGGER.debug('\tresponse code:%s', response.status_code)

        try:
            LOGGER.debug('\tresponse: %s', response.json())
        except ValueError:
            LOGGER.debug('\tresponse: %s', response.content)

        return response

    def list_jobs(self):
        """ API call to get all jobs """
        return self._api_request(
            'jobs',
            'GET'
        )

    def create_job(self, payload=None):
        """ API call to create a job """
        return self._api_request(
            'jobs',
            'POST',
            payload=payload
        )

    def get_job(self, job_id):
        """ API call to get a specific job """
        return self._api_request(
            'jobs/%s' % job_id,
            'GET'
        )

    def update_job(self, job_id, payload=None):
        """ API call to update a specific job """
        return self._api_request(
            'jobs/%s' % job_id,
            'PUT',
            payload=payload
        )

    def delete_job(self, job_id):
        """ API call to delete a specific job """
        return self._api_request(
            'jobs/%s' % job_id,
            'DELETE'
        )

    def process_job(self, job_id):
        """ API call to process a specific job """
        return self._api_request(
            'jobs/%s/process' % job_id,
            'POST'
        )

    def cancel_job(self, job_id):
        """ API call to cancel a specific job """
        return self._api_request(
            'jobs/%s/cancel' % job_id,
            'POST'
        )

    def list_profiles(self):
        """ API call to get all profiles """
        return self._api_request(
            'profiles',
            'GET'
        )

    def create_profile(self, payload=None):
        """ API call to create a profile """
        return self._api_request(
            'profiles',
            'POST',
            payload=payload
        )

    def get_profile(self, profile_id):
        """ API call to get a specific profile """
        return self._api_request(
            'profiles/%s' % profile_id,
            'GET'
        )

    def update_profile(self, profile_id, payload=None):
        """ API call to update a specific profile """
        return self._api_request(
            'profiles/%s' % profile_id,
            'PUT',
            payload=payload
        )

    def delete_profile(self, profile_id):
        """ API call to delete a specific profile """
        return self._api_request(
            'profiles/%s' % profile_id,
            'DELETE'
        )

    def list_photos(self):
        """ API call to get all photos """
        return self._api_request(
            'photos',
            'GET'
        )

    def create_photo(self, payload=None):
        """ API call to create a photo """
        return self._api_request(
            'photos',
            'POST',
            payload=payload
        )

    def get_photo(self, photo_id):
        """ API call to get a specific photo """
        return self._api_request(
            'photos/%s' % photo_id,
            'GET'
        )

    def update_photo(self, photo_id, payload=None):
        """ API call to update a specific photo """
        return self._api_request(
            'photos/%s' % photo_id,
            'PUT',
            payload=payload
        )

    def delete_photo(self, photo_id):
        """ API call to delete a specific photo """
        return self._api_request(
            'photos/%s' % photo_id,
            'DELETE'
        )
