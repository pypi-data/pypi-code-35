"""
Fiddler python client.
"""
# TODO: Add License

import json
import requests


class FiddlerException(Exception):
    """An exception raised by client API in case of errors."""
    pass


API_BASE_URL = 'http://api.fiddler.ai'  # TODO: Change to https.


class Fiddler:
    """
    :param token: Token for Fiddler API (available under account settings
                   on https://fiddler.ai).
    :param organization: Name of the organization
    :param project: Project for the model
    :param model_id: Model name or similar identifier
    """

    def __init__(self, token, organization, project, model_id=None):
        self.token = token
        self.organization = organization
        self.project = project
        self.model_id = model_id
        self._sender = _RequestSender()  # Tests could set an alternate sender.

    def publish_event(self, event):
        """
        Publishes an event to Fiddler Service.
        :param dict event: Dictionary of event details, such as features
                           and predictions.
        """
        # More candidates for args: timestamp, or any specific details?
        api_endpoint = '{base}/external_event/{org}/{project}/{model}'.format(
            base=API_BASE_URL.rstrip('/'),
            org=self.organization,
            project=self.project,
            model=self.model_id
        )
        self._sender.send(api_endpoint, self.token, event)


class _RequestSender:
    """
    Sends events to Fiddler API service and handles HTTP reponse and errors.
    """

    @staticmethod
    def send(api_endpoint, token, data):
        """
        Sends HTTP Post request to api_endpoint.
        :param api_endpoint: e.g. http://api.fiddler.com/
        :param token: token to send with the request.
        :param data: dictionary, which is sent as as JSON.
        :raises FiddlerException in case of
        errors or if the response from server does not indicate 'SUCCESS'.
        """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(token)
        }

        try:
            resp = requests.post(api_endpoint,
                                 data=json.dumps(data),
                                 headers=headers)
        except requests.RequestException as e:
            raise FiddlerException(e)

        resp_json = None

        try:
            resp_json = resp.json()
        except ValueError:
            pass  # will throw right below to avoid nested exceptions.

        if not resp_json:
            # Server didn't send proper json response. It should.
            raise FiddlerException('Error response from server: {}{}'.format(
                resp.text[0:150],
                len(resp.text) > 150 and '...'
            ))

        if resp_json.get('status') != 'SUCCESS':
            error_msg = json.get('message', 'Unknown error from server')
            raise FiddlerException(error_msg)
