import requests

from lambdabase.LambdaException import RemoteCallException
from lambdabase.invokers import Invoker


class HttpPostInvoker(Invoker):
    """
    Invoker class for making lambda to lambda calls when
    running inside the Flask endpoint environment.
    """
    HOST = 'http://{}:{}'.format('localhost', 5000)
    _client = None

    def __init__(self, function_name, request_type, response_type, async_event=False):
        super(HttpPostInvoker, self).__init__(function_name, request_type, response_type)
        self.async_event = async_event

    def invoke(self, request):
        """
        Invoke the remote procedure
        :param request: the request object
        :return: an object of type response_type
        """
        endpoint = '{}/{}'.format(self.HOST, self.function_name)
        response = requests.post(endpoint, json=request.data)

        if response.status_code == 200:
            response = response.json()
            return self.response_type(response)
        if response.status_code == 204:
            return None
        if response.status_code == 500:
            raise RemoteCallException('Invoking remote function [{}] failed: [{}]'
                                      .format(self.function_name, response.reason))

        return None



