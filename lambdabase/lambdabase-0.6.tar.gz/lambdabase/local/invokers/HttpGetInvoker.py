import requests

from lambdabase.LambdaException import RemoteCallException
from lambdabase.ambdas.invokers.Invoker import Invoker


class HttpGetInvoker(Invoker):
    """
    Invoker class for making lambda to lambda calls when
    running inside the Flask endpoint environment.
    """
    HOST = 'http://{}:{}'.format('localhost', 5000)
    _client = None

    def __init__(self, function_name, request_type, response_type, extract_query=None, resource_index=None, async_event=False):
        super(HttpGetInvoker, self).__init__(function_name, request_type, response_type)
        self.async_event = async_event
        self.resource_index = resource_index
        self.extract_query = extract_query

    def invoke(self, request):
        """
        Invoke the remote procedure
        :param request: the request object
        :return: an object of type response_type
        """
        if self.resource_index is None:
            endpoint = '{}/{}'.format(self.HOST, self.function_name)
        else:
            endpoint = '{}/{}/{}'.format(self.HOST, self.function_name, request.data[self.resource_index])

        params = {}
        if self.extract_query is not None:
            params = {self.extract_query: request.data[self.extract_query]}

        response = requests.get(endpoint, params=params)

        if response.status_code == 200:
            response = response.json()
            return self.response_type(response)
        if response.status_code == 204:
            return None
        if response.status_code == 500:
            raise RemoteCallException('Invoking remote function [{}] failed: [{}]'
                                      .format(self.function_name, response.reason))

        return None



