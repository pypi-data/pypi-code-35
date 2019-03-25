import click


class Logger(object):
    def __init__(self, config):
        self.__config = config

    def _verbose(self, message):
        """
        Helper method to wrap verbose messages stylistically.

        :param message: String message to print.
        :return: None
        """
        if self.__config.verbose: self.__display(message, 'blue')

    def _warn(self, message):
        """
        Helper method to wrap warning messages stylistically.

        :param message: String message to print.
        :return: None
        """
        self.__display(message, 'yellow')

    def _error(self, message):
        """
        Helper method to wrap error messages stylistically.

        :param message: String message to print.
        :return: None
        """
        self.__display(message, 'red')

    def _success(self, message):
        """
        Helper method to wrap success messages stylistically.

        :param message: String message to print.
        :return: None
        """
        self.__display('{}'.format(message), 'green')

    def _request_log(self, method_type, url, status_code, data):
        """
        Helper method to log http requests stylistically.

        :param method_type: REST method used.
        :param url: endpoint hit.
        :param status_code: response status.
        :param data: response data.
        :return:
        """
        self._verbose('{} {} and status code was {}'.format(method_type, url, status_code))
        self._verbose('Data received {}'.format(data))

    def __display(self, message, color):
        """
        Internal method to print message.

        :param message: formatted message to print
        :param icon: icon to prefix message with
        :param color: color of the message
        :return: None
        """
        click.secho('{}'.format(message), fg=color)
