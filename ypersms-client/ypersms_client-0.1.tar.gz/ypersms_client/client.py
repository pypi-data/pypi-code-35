"""
Client for YperSMS project.
"""
import requests


class ClientError(Exception):
    """
    Generic client error.
    """
    pass


class YperSMSClient(object):
    """
    Client class for YperSMS.
    """

    def __init__(self, base_url, client_id, client_secret):
        """
        :param str base_url: ypersms api base url
        :param str client_id:
        :param str client_secret:
        """
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret

        self._login()

    def _api_url(self, path):
        """
        Generate correct uri for requests.

        :param string path: desired url path
        :rtype: string
        """
        return f'{self.base_url}/{path}'

    def _login(self):
        """
        Login into the API.
        """
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials',
        }
        req = requests.post(self._api_url('oauth/token'), json=payload)
        if req.status_code != 200:
            raise ClientError(f'Failed to authenticate ({req.status_code})')

        self._token_infos = req.json()

    def get_senders(self):
        """
        Retreive available sender ids.

        :rtype: list
        """
        req = requests.get(self._api_url('sms/sender'))
        if req.status_code != 200:
            raise ClientError(f'Failed to get senders ({req.status_code})')

        return req.json()['result']

    def send(self, recipients, message, sender_id=None):
        """
        Send a message.

        :param list recipients:
        :param str message:
        :param str sender_id: who is the sender
        :returns: used credits
        :rtype: int
        """
        if sender_id is None:
            sender_id = self.get_senders().pop()

        payload = {
            'sender_id': sender_id,
            'recipients': recipients,
            'message': message
        }
        req = requests.post(self._api_url('sms/send'), json=payload)
        if req.status_code != 200:
            raise ClientError(f'Failed to send message ({req.status_code})')

        return req.json()['total_credit_used']
