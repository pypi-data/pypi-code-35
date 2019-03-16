from abc import ABCMeta, abstractmethod

from lambdabase.Request import Request


class Invoker(object):
    """
    Abstract base class for invokers. Invokers are used for
    making inter-lambda calls with different variants for
    when running locally or in the cloud
    """
    __metaclass__ = ABCMeta

    def __init__(self, function_name, request_type, response_type):
        if not isinstance(request_type, Request.__class__):
            raise InvokerException('Attempted to register a request object which '
                                   'does not extend the base Request object')

        self.request_type = request_type
        self.response_type = response_type
        self.function_name = function_name

    @abstractmethod
    def invoke(self, request):
        pass


class InvokerException(Exception):
    pass
