import json
import requests

from collections import OrderedDict
from superofficesdk.login import SuperOfficeLogin

try:
    from urlparse import urljoin
except ImportError:
    # Python 3+
    from urllib.parse import urljoin

API_VERSION = 'v1'


class SuperOffice():

    def __init__(self,
                 cust_id=None,
                 app_token=None,
                 sys_token=None,
                 private_key=None,
                 username=None,
                 password=None,
                 environment='online'):
        self.cust_id = cust_id
        self.app_token = app_token
        self.sys_token = sys_token
        self.private_key = private_key
        self.environment = environment

        self.session = requests.Session()

        if all(arg is not None for arg in (
               username, password, environment)):

            self.auth_type = 'basic'

            self.ticket = SuperOfficeLogin(
                self.cust_id,
                self.app_token,
                self.sys_token,
                self.private_key,
                self.environment)

        elif all(arg is not None for arg in (
                 cust_id, app_token, sys_token, private_key, environment)):

            self.auth_type = 'SOTicket'

            self.ticket = SuperOfficeLogin(
                self.cust_id,
                self.app_token,
                self.sys_token,
                self.private_key,
                self.environment)

        else:
            raise TypeError(
                'You must provide login information or token/ticket'
            )

        self.base_url = ('https://{env}.superoffice.com/{cust}/api/{ver}/'
                         .format(env=self.environment,
                                 cust=self.cust_id,
                                 ver=API_VERSION))

        self.headers = {
            'Authorization': 'SOTicket %s' % self.ticket,
            'SO-AppToken': self.app_token,
            'Content-Type': 'application/json',
        }

    def __getattr__(self, name):
        """"Returns an 'SOType' instance for the given SuperOffice object type

        Arguments:

        * name -- the name of a SuperOffice object type, e.g. Contact or Person

        """

        if name.startswith('__'):
            return super(SuperOffice, self).__getattr__(name)

        return SOType(name, self.cust_id,
                      self.environment, API_VERSION,
                      self.session, self.ticket, self.app_token)

    def query(self, entity, fields, filter=None, skip=None, top=None, format='json'):
        url = self.base_url + entity

        params = {
            '$select': fields,
            '$format': format
        }
        if filter:
            params.update({'$filter': filter})
        if skip:
            params.update({'$skip': skip})
        if top:
            params.update({'$top': top})

        result = self._call_superoffice('GET', url, params=params)
        print(result.text)
        return result.json(object_pairs_hook=OrderedDict)

    def call_superoffice(self, method, url, **kwargs):

        result = self.session.request(
            method, url, headers=self.headers, **kwargs)

        # TODO: handle exceptions

        return result


class SOType(object):
    """An interface to a specific type of SuperOffice Type"""

    def __init__(self, entity_name, cust_id,
                 environment, api_version,
                 session, auth, app_token):

        self.entity_name = entity_name
        self.session = session
        self.auth = auth
        self.app_token = app_token

        self.base_url = ('https://{env}.superoffice.com/{cust}/api/{ver}/{entity}/'
                         .format(env=environment,
                                 cust=cust_id,
                                 ver=api_version,
                                 entity=entity_name))

    def get(self, id, headers=None):
        """Returns th result of a GET request to '/api/{version}/{entity_name}/{id}

        * id -- the Id of the SOObject to get.
        * headers -- a dict with additional request headers.
        """

        result = self._call_superoffice(
            method='GET', url=urljoin(self.base_url, id),
            headers=headers
        )

        return result.json(object_pairs_hook=OrderedDict)

    def create(self, data, headers=None):
        """Creates a new SOObject using POST '/api/{version}/{entity_name}/'

        Arguments:

        * data -- a dict of the data to create the SuperOffice Object from.
        * headers -- a dict with additional request headers
        """

        result = self._call_superoffice(
            method='POST', url=self.base_url,
            data=json.dumps(data), headers=headers
        )

        return result.json(object_pairs_hook=OrderedDict)

    def update(self, id, data, raw_response=False, headers=None):
        """Updates an SuperOffice Object using PUT tp '/api/{version}/{entity_name}/{id}'.id

        Arguments:

        * id -- the Id of the SuperOffice Object to update
        * data -- a dict of the data to update the SuperOffice Object from.
        * raw_response -- a boolean indicating whether to return the response
                          directly instead of the status code.id
        * headers -- a dict with additional request headers.
        """

        result = self._call_superoffice(
            method='PUT', url=urljoin(self.base_url, id),
            data=json.dumps(data), headers=headers
        )

        return self._raw_response(result, raw_response)

    def delete(self, id, headers=None):
        """Deletes an SuperOffice Object using DELETE to '/api/{version}/{entity_name}/{id}'

        Arguments:
        * id -- the Id of the SuperOffice Object to delete
        * headers -- a dict with additional request headers.
        """

        result = self._call_superoffice(
            method='DELETE', url=urljoin(self.base_url, id),
            headers=headers
        )

        return self._raw_response(result, False)

    def _call_superoffice(self, method, url, **kwargs):

        headers = {
            'Authorization': 'SOTicket %s' % self.auth,
            'SO-AppToken': self.app_token,
            'Content-Type': 'application/json',
            'Accept': 'aplication/json'
        }

        additional_headers = kwargs.pop('headers', dict())
        headers.update(additional_headers or dict())

        result = self.session.request(
            method, url, headers=headers, **kwargs)

        # TODO: handle exceptions

        return result

    def _raw_response(self, response, flag):
        """Utility method returning either the status code
           or the body of the request

        Arguments:

        * response -- the raw response
        * flag -- a boolean indicatinf whether to return the response
                  directly instead of the status code.
        """

        if not flag:
            return response.status_code

        return response
