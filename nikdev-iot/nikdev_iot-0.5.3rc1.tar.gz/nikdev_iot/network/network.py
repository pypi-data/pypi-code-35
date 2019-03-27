# -*- coding: utf-8 -*-

import requests
from nikdev_iot.config import Config


class Network:
    """
    Helper class that wraps the requests function with header data and timeout configuration.
    """

    config = None
    """
    The configuration object for the network class.

    :type: Config
    """

    def __init__(self, config):
        """
        Initializes a network class that helps the requests by adding authorization headers and meta data to the request.

        :param Config config: The configuration settings for the Api call.
        """
        self.config = config

    def get_headers(self):
        """
        Gets the headers from the configuration that are needed to communicate with the server.
        :return: The provided headers for communicating with the server.
        :rtype: dict[str, str]
        """
        return {
            'x-device-id': self.config.get_value('deviceId'),
            'x-api-key': self.config.get_value('apiKey')
        }

    def get_timeout(self):
        """
        Gets the preferred timeout setting from the configuration.
        :return: The timeout set in seconds.
        :rtype: int
        """
        return self.config.get_value('requestTimeout')

    def post(self, url, json):
        """
        Transmits data to the server with applied headers and configurations.

        :param url:     The url to post to.
        :param json:    The data to provide to the server.
        :return:        A tuple existing of an int and the response object. The int is an enum of the
                        NetworkStatus class to simplify whether or not to stage the data after failure.
        :rtype: (int, requests.Response)
        """
        return self.request(
            requests.post,
            url=url,
            json=json,
            headers=self.get_headers(),
            timeout=self.get_timeout()
        )

    def get(self, url):
        """
        Fetches data from the server with applied headers and configurations.

        :param url:     The url to get from.
        :return:        A tuple existing of an int and the response object. The int is an enum of the
                        NetworkStatus class to simplify whether or not to stage the data after failure.
        :rtype: (int, requests.Response)
        """
        return self.request(
            requests.get,
            url=url,
            headers=self.get_headers(),
            timeout=self.config.get_value('requestTimeout')
        )

    @staticmethod
    def request(func, **args):
        """
        Helper function to do requests and not rewriting a lot of code. This method should only be used by post and get.

        :param func:    The The request function to run.
        :param args:    The arguments to pass on to the request function
        :return:        A tuple existing of an int and the response object. The int is an enum of the
                        NetworkStatus class to simplify whether or not to stage the data after failure.
        :rtype: (int, requests.Response)
        """
        # Declare empty return values
        response = None
        status = NetworkStatus.SUCCESS
        # Make a try to request, but catch if there's a timeout
        try:
            # Do the provided request
            response = func(**args)
            if not response.ok:
                if response.status_code >= 500:
                    # If the request failed and there's an error from the server, it's just bad luck (presumably)
                    status = NetworkStatus.BAD_LUCK
                else:
                    # If there wasn't a server error its a 400 error and was probably something wrong with the request.
                    status = NetworkStatus.BAD_REQUEST
        except requests.exceptions.Timeout:
            # There's a timeout, most likely bad luck
            status = NetworkStatus.BAD_LUCK

        # Return as tuple
        return status, response


class NetworkStatus:
    """
    Enum class which only purpose hold values to represent the status requests.
    """

    SUCCESS = 200
    """
    Simplified status code if the request went ok.
    """
    BAD_REQUEST = 400
    """
    Simplified status code if there was something wrong with the provided data (ie bad api key).
    Basically a reason to not try again.
    """

    BAD_LUCK = 500
    """
    Simplified status code if there was something wrong with the server or timeout.
    Basically a reason to not try again later.
    """
