from abc import ABCMeta, abstractmethod


class UnhandledProviderException(Exception):
    """ Unhandled Exception """

    def __init__(self, msg):
        self.message = msg


class RecordNotFound(Exception):
    """ Record Not Found Exception """

    def __init__(self, msg):
        self.message = msg


class BaseProvider():
    """ Base NOSQL Provider """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_record(self, model, table, **kwargs):
        """ Get a single record from DB

        :param model: obj BaseModel
        :param table: str table
        :return: dict record
        :raises: ClientException
        """

    @abstractmethod
    def get_records(self, model, table, **kwargs):
        """ Get multiple records from DB

        :param model: obj BaseModel
        :param table: str table
        :param options: obj options
        :return: list records
        :raises: ClientException
        """

    @abstractmethod
    def scan_records(self, model, table, **kwargs):
        """ Get multiple records from DB through scan without index

        :param model: obj BaseModel
        :param table: str table
        :param options: obj options
        :return: list records
        :raises: ClientException
        """

    @abstractmethod
    def put_record(self, model, table, **kwargs):
        """ Put record into DB

        :param model: obj BaseModel
        :param table: str table
        :return: bool status
        :raises: ClientException
        """

    @abstractmethod
    def delete_record(self, model, table, **kwargs):
        """ Delete record from DB

        :param model: obj BaseModel
        :param table: str table
        :return: bool status
        :raises: ClientException
        """
