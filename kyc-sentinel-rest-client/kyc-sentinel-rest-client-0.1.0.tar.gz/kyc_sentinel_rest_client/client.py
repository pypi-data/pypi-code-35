import requests
import os
from datetime import datetime
from urllib.parse import urljoin
from .config import Config
from .client_helper import BearerAuth, post_update_logs_payload

class Client():
    '''
      simple client for KYC Sentinel
    '''
    AUTH_PATH = Config.AUTH_PATH 
    UPDATE_LOGS_PATH = Config.UPDATE_LOGS_PATH
    INDIVIDUALS_QUERIES_PATH = Config.INDIVIDUALS_QUERIES_PATH
    DATETIME_FORMAT = Config.DATETIME_FORMAT

    class RequireAuth():
        def __call__(self, func):
            def wrapper(self, auth_token = None, **kwargs):
                if auth_token is not None:
                    return func(self, auth_token = auth_token, **kwargs)
            return wrapper

    def __init__(self, **kwargs):
        self.root_url = kwargs.get('root_url')
        self.auth_url = urljoin(self.root_url, self.AUTH_PATH)
        self.update_logs_url = urljoin(self.root_url, self.UPDATE_LOGS_PATH)
        self.individual_queries_url = urljoin(self.root_url, self.INDIVIDUALS_QUERIES_PATH)

    def get(self, full_url, id = None, auth=None, **kwargs):
        '''generic GET'''
        if id is not None:
            full_url = os.path.join(full_url, str(id))
        return requests.get(full_url, auth = auth, params = kwargs) 
    
    def post(self, full_url, auth = None, record = None):
        '''generic POST'''
        return requests.post(full_url, auth = auth, json = record)

    def auth(self, email = None, password = None):
        '''POST credentials to obtain tokens'''
        record = { 'email': email, 'password': password }
        return self.post(self.auth_url, record = record)

    @RequireAuth()
    def post_update_logs(self, auth_token = None, **kwargs):
        '''POST update_logs to inform about newly updated records'''
        category = kwargs.get('individual') or 'individual'
        return self.post(self.update_logs_url,
                    auth = BearerAuth(auth_token),
                    record = post_update_logs_payload(category = category, datetime_format = self.DATETIME_FORMAT, **kwargs)
                    )


