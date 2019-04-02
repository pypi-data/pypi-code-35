"""
Python Lotame API wrapper.
==========================
Filename: lotame.py
Author: Paulo Kuong
Email: pkuong80@gmail.com
Python Version: 3.6.1

Please refer to https://api.lotame.com/docs/#/ to get all Endpoints.
Please refer to README for examples.
"""
from contextlib import contextmanager
from functools import wraps
import os
import requests
import time
from urllib.parse import urlencode


class Audience(object):
    """Audience related code.
    """

    def get_create_audience_json(
            self, audience_name, client_id, behavior_groups, description='',
            condition_between_grouops='OR', condition_within_group='AND',
            **custom_request_params):
        """Constructs minimal json audience definition.

        behavior_groups (list): list of behavior ids.
            For example: [[244, 343, 345], [33, 235]]
            Where there is AND condition between ids in the sub list, and
            OR condition on the groups of sub lists, that is:
            [[244 AND 343 AND 345] OR [33 AND 235]]

        Args:
            audience_name (str): audience name.
            client_id (int): id of client this audience should belong to.
            behavior_groups (list): 2 dimensional list of behavior ids.
            description (str[optional]): description of this audience.
            condition_between_grouops (str[optional]): condition between groups of behaviors.
            condition_within_group (str[optional]): condition within each group of behaviors.
            custom_request_params (dict): custom request params.
        Returns:
            dict: audience definition:
                {
                  'name': audience_name,
                  'clientId': client_id,
                  'definition': ....,
                  'description': '.......'
                }
        """
        component = []
        for index, behavior_group in enumerate(behavior_groups):
            tmp = {
                'operator': None
            }
            if len(behavior_group) == 1:
                tmp['complexAudienceBehavior'] = {
                    'purchased': True,
                    'behavior': {
                        'id': behavior_group[0]
                    },
                }
            else:
                tmp['component'] = []
                for index2, behavior in enumerate(behavior_group):
                    tmp2 = {
                        'operator': None,
                        'complexAudienceBehavior': {
                            'purchased': True,
                            'behavior': {
                                'id': behavior
                            }
                        }
                    }
                    if index2 != 0:
                        tmp2['operator'] = condition_within_group
                    tmp['component'].append(tmp2)
            if index != 0:
                tmp['operator'] = condition_between_grouops
            component.append(tmp)

        definition = {
            'name': audience_name,
            'clientId': client_id,
            'definition': {'component': component}
        }
        if len(custom_request_params.items()) > 0:
            for k, v in custom_request_params.items():
                if k not in ['name', 'clientId', 'definition']:
                    definition[k] = v
        if 'overlap' not in definition:
            definition['overlap'] = True

        if description:
            definition['description'] = description
        return definition


class Lotame(Audience):
    """Main class for handling low level operations.
    For endpoint specific code, please create classes above,
    drop the code there and extend the class as mixin.
    """
    API_URL = 'https://api.lotame.com/2'
    AUTH_URL = 'https://crowdcontrol.lotame.com/auth/v1/tickets'
    MAX_RETRIES = 10

    def __init__(self, username='', password='', debug=False):
        self._debug = debug
        self._username = username or os.getenv('LOTAME_USERNAME')
        self._password = password or os.getenv('LOTAME_PASSWORD')

    def _retry_request_decorator(max_retries):
        def _retry_request_sub_decorator(request):
            @wraps(request)
            def wrapper(*args, **kargs):
                status_code = ''
                fib_num_a = 1
                fib_num_b = 1
                retry = 0
                response = request(*args, **kargs)
                status_code = response.status_code

                while (status_code == '' or status_code == 500) and retry <= max_retries:
                    response = request(*args, **kargs)
                    status_code = response.status_code
                    new_interval = fib_num_b + fib_num_a
                    fib_num_a = fib_num_b
                    time.sleep(new_interval)
                    fib_num_b = new_interval
                    retry += 1

                if retry > max_retries:
                    raise Exception(
                        'Maximum retries exceeded. Response object '
                        'dump: {}'.format(
                            response))
                return response

            return wrapper

        return _retry_request_sub_decorator

    @contextmanager
    def _authenticate(self):
        """Authenticate user and get TGT (Ticket granting ticket).
        """
        res = requests.post(self.AUTH_URL, data={
            'username': self._username,
            'password': self._password
        })
        assert (
            'location' in res.headers and res.headers['location']
        ), 'Authentication Failed!'
        tgt = res.headers['location']
        yield tgt
        requests.delete(tgt)

    def _get_service_ticket_token(self, tgt, end_point):
        """Get TGT ticket token for an end_point.

        Args:
            tgt (str): tgt from authentication response.
            end_point (str): desired end point.
        Returns:
            Ticket token: ticket token generated.
        """
        return requests.post(
            tgt, data={
                'service': '{}/{}'.format(self.API_URL, end_point)
            }).text

    @_retry_request_decorator(MAX_RETRIES)
    def get(self, end_point, **params):
        """Make GET request with params with ticket token sent along.

        Args:
            end_point (str): desired endpoint.
            params (dict): available params for that endpoint.
        Returns:
            Response object.
        """
        with self._authenticate() as tgt:
            end_point_with_params = end_point
            if len(params) > 0:
                end_point_with_params = '{}?{}'.format(
                    end_point, urlencode(params))

            service_ticket = self._get_service_ticket_token(
                tgt, end_point_with_params)
            ticket_param = '&ticket={}'.format(service_ticket)
            if end_point_with_params.find('?') == -1:
                ticket_param = '?ticket={}'.format(service_ticket)
            if self._debug:
                print('{}/{}{}'.format(
                    self.API_URL,
                    end_point_with_params, ticket_param))

            print('{}/{}{}'.format(self.API_URL, end_point_with_params,
                                   ticket_param))
            return requests.get(
                '{}/{}{}'.format(self.API_URL, end_point_with_params,
                                 ticket_param))

    @_retry_request_decorator(MAX_RETRIES)
    def post(self, end_point, params):
        """Make POST request with params with ticket token sent along.

        Args:
            end_point (str): desired endpoint.
            params (dict): available params for that endpoint.
        Returns:
            Response object
        """
        with self._authenticate() as tgt:
            service_ticket = self._get_service_ticket_token(tgt, end_point)
            if self._debug:
                print(params)
                print('{}/{}?ticket={}'.format(
                    self.API_URL, end_point, service_ticket))

            return requests.post(
                '{}/{}?ticket={}'.format(
                    self.API_URL, end_point, service_ticket), json=params)

    def delete(self, end_point):
        """Make DELETE request with ticket token sent along.

        *Note that there is no decorator for retry, for safety reason.

        Args:
            end_point (str): desired endpoint.
        Returns:
            Response object
        """
        with self._authenticate() as tgt:
            service_ticket = self._get_service_ticket_token(tgt, end_point)
            response = requests.delete('{}/{}?ticket={}'.format(
                self.API_URL, end_point, service_ticket))
            return response
