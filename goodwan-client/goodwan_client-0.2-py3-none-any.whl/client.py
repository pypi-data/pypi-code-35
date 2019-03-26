"""
GoodWan client library: client class
"""
import json
import logging

import requests.exceptions
from pytz import timezone

from goodwan_client.event import Event
from goodwan_client.errors import CommunicationError, ParseError, ProtocolError
from goodwan_client.helpers import datetime_to_str
from goodwan_client.serializer import Serializer

logger = logging.getLogger("goodwan")


class Client:
    """
    GoodWan client class
    """

    URL_TEMPLATE = "https://api.goodwan.ru/v1/{method}"
    TIMEOUT = 30

    def __init__(self, login, password, timezone_name="UTC"):
        """
        Constructor
        :param login: API login
        :type login: str
        :param password: API password
        :type password: str
        :param timezone_name: local timezone name
        :type timezone_name: str
        """
        self.login = login
        self.password = password
        self.requests = requests
        self.timezone = timezone(timezone_name)
        self._sr = Serializer(self.timezone)

    def call(self, method_name, parameters):
        """
        Call method
        :param method_name: method name
        :type method_name: str
        :param parameters: method parameters
        :type parameters: dict
        :return: decoded result dictionary
        :rtype: dict|list
        """
        # Make request
        url = self.URL_TEMPLATE.format(method=method_name)
        auth = (self.login, self.password)

        try:
            request = requests.Request(method="GET", url=url,
                                       params=parameters, auth=auth)
            p_request = request.prepare()
            logger.debug("Making HTTP request: {}".format(p_request.url))
            with requests.sessions.Session() as session:
                result = session.send(p_request, timeout=self.TIMEOUT)

        except requests.exceptions.ConnectionError as err:
            raise CommunicationError("Connection error: {}".format(err))
        logger.debug("Got HTTP reply ({}): {}"
                     .format(result.status_code, result.text))

        # HTTP code
        if result.status_code == 401:
            raise ProtocolError("(401) Authentication error")
        elif result.status_code == 403:
            raise ProtocolError("(403) Forbidden")
        elif result.status_code == 404:
            raise ProtocolError("(404) Not Found")
        elif result.status_code != 200:
            raise ProtocolError("HTTP error ({}): {}"
                                .format(result.status_code, result.text))

        # Decode result
        try:
            decoded = json.loads(result.text)
            assert isinstance(decoded, (dict, list)), "wrong result type"
        except (AssertionError, json.JSONDecodeError) as err:
            raise ParseError("Result parse error: {} (\"{}\")"
                             .format(err, result.text))

        return decoded

    def events(self, t_from=None, t_to=None, e_type=None, e_count=None,
               device_id=None):
        """
        Get device events
        :param t_from: period start, optional
        :type t_from: datetime.datetime
        :param t_to: period end, optional
        :type t_to: datetime.datetime
        :param e_type: event type, optional
        :type e_type: int
        :param e_count: event count, optional
        :type e_count: int
        :param device_id: device ID, optional
        :type device_id: int
        :return: list[goodwan_client.classes.Event]
        """
        # Call
        parameters = {}
        if t_from is not None:
            parameters["from"] = datetime_to_str(t_from, self.timezone)
        if t_to is not None:
            parameters["to"] = datetime_to_str(t_to, self.timezone)
        if e_type is not None:
            parameters["type"] = int(e_type)
        if e_count is not None:
            parameters["count"] = int(e_count)
        if device_id is not None:
            parameters["deviceId"] = int(device_id)

        # Objectify
        call_result = self.call("events", parameters)
        if not isinstance(call_result, list):
            raise ParseError("Result parse error: not a list")
        try:
            result = list(self._sr.objectify(e, Event) for e in call_result)
        except ParseError as err:
            raise ParseError("Result parse error: {}".format(err))

        return result
