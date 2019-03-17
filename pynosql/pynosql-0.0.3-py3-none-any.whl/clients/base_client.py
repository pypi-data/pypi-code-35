from abc import ABCMeta, abstractmethod, abstractproperty


class InitializationError(Exception):
    """ Exception initializing client """

    def __init__(self, msg):
        self.message = msg


class ClientException(Exception):
    """ Exception calling client method """

    def __init__(self, msg):
        self.message = msg


class BaseClient():
    """ Base Client """

    __metaclass__ = ABCMeta

    @abstractproperty
    def client(self):
        """ Client property

        :return: obj client
        """

    @abstractmethod
    def initialize(self):
        """ Initialize client

        :return: obj client/session
        """

    @abstractmethod
    def call(self, client_method, **kwargs):
        """ Call client method

        :param client_method: str method
        :param kwargs: obj args
        :return: obj restuls
        """
