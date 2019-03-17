from abc import ABCMeta, abstractmethod


class InvalidCredentials(Exception):
    """ Invalid Credentials Exception

        Check if the credentials are not None and are
        valid strings.

    """
    def __init__(self, msg):
        self.message = msg


class BaseCredentials():
    """ Base Credentials Class """

    __metaclass__ = ABCMeta

    @abstractmethod
    def check_credentials(self):
        """ Check for valid credentials

        :return: None
        :raises: InvalidCredentials
        """
