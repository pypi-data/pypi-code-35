import json
import requests
from urllib.parse import urlencode, urljoin

class DeepTraceClient():
    def __init__(self, url_base=None):
        self.url_base = url_base

    def __get_auth(self, kwargs):
        return (kwargs.get('username'), kwargs.get('password')) \
            if kwargs.get('username') and kwargs.get('password') is not None \
            else None

    def __get(self, path=None, auth=None, query=None, headers=None):
        url = urljoin(self.url_base, path)
        return requests.get(url, headers='headers', params=query, auth=auth)

    def __post(self, path=None, body={}, auth=None, headers=None):
        url = urljoin(self.url_base, path)
        return requests.post(url, headers=headers, auth=auth, data=body)
    
    def fetchTraceById(self, id, **kwargs):
        auth = self.__get_auth(kwargs)
        return self.__get('/v1/traces/{}'.format(id), auth=auth).json()

    def createTrace(self, trace, **kwargs):
        auth = self.__get_auth(kwargs)
        headers = {'Content-Type': 'application/json' }
        data = json.dumps(trace, ensure_ascii=False)
        self.__post('/v1/traces', body=data, auth=auth, headers=headers)

        #  TODO: catch exceptions