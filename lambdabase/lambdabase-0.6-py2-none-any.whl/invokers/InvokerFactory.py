from abc import ABCMeta, abstractmethod


class InvokerFactory(object):
    """
    Base class for the invoker factories
    """
    __metaclass__ = ABCMeta

    invokers = {}

    def invoke(self, name, body):
        """
        Make a call to the initialised invoker
        :param name: the name of the invoker to call
        :param body: the body to pass to the invoker
        :return: the results of the invoked function
        """
        if name not in self.invokers:
            raise ValueError('Specified invoker is not available [{}]'.format(name))
        return self.invokers[name].invoke(body)

    @abstractmethod
    def register(self, service, function_name, source_type, result_type, query_key, invoker_type):
        """
        Register an invoker with the InvokerFactory
        :param service: The name of the service
        :param function_name: The name of the function
        :param source_type: The type of the request object
        :param result_type: The type of the result object
        :param query_key: Optional key into the request object
        to determine query arguments when invoking another lambda/gateway
        :param invoker_type: The type of the Invoker to be used
        :return: The result of the request as an object of type result_type
        """
        pass

    @abstractmethod
    def get_function_name(self):
        pass
