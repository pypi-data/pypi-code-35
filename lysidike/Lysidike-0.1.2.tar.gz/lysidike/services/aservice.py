from pelops.logging import mylogger


class AService:
    """
    Abstract service - an implementation of it provides everything that is needed to publish the message
    to a messaging service like email or to output it to e.g. stdout.

    Abstact service has no config yaml entries.
    """

    _mqtt_client = None  # mqtt_client instance
    _logger = None  # logger
    _config = None  # yaml config structure
    last_message = None  # contains the last rendered message

    def __init__(self, config, mqtt_client, logger_name, logger):
        """
        Constructor

        :param config: yaml config structure
        :param mqtt_client: mqtt_client instance
        :param logger: logger instance from the parent. a child will be spawned
        :param logger_name: name for the child instance
        """
        self._logger = mylogger.get_child(logger, logger_name)
        self._mqtt_client = mqtt_client
        self._config = config

        self._logger.info("{}.__init__".format(self.__class__.__name__))
        self._logger.debug("{}.__init__ config: {}".format(self.__class__.__name__, self._config))

    def start(self):
        """
        start the service - calls self._start and
        :raises RuntimeError if self._test_connection returns fals
        """
        self._logger.info("{}.start - starting".format(self.__class__.__name__))
        self._start()
        if not self._test_connection():
            self._logger.error("{}.start - connection test failed".format(self.__class__.__name__))
            raise RuntimeError("{}.start - connection test failed".format(self.__class__.__name__))
        self._logger.info("{}.start - started".format(self.__class__.__name__))

    def stop(self):
        """
        stops the service - calls self._stop
        """
        self._logger.info("{}.stop - stopping".format(self.__class__.__name__))
        self._stop()
        self._logger.info("{}.stop - stopped".format(self.__class__.__name__))

    def publish(self, subject, messages):
        """
        Publish the topics to this service

        :param subject: string - subject for message
        :param messages: list of topics to be published. each entry is a tuple (datetime, topic, message)
        """
        self._logger.info("{}.publish - starting".format(self.__class__.__name__))
        self._logger.debug("{}.publish - subject: '{}', len messages: {}, messages: {}"
                           .format(self.__class__.__name__, subject, len(messages), messages))

        self.last_message = self._render_message(messages)
        self._logger.debug("{}.publish - message: ".format(self.__class__.__name__, self.last_message))

        self._send_message(subject, self.last_message)

        self._logger.info("{}.publish - finished".format(self.__class__.__name__))

    def _start(self):
        """
        initialise service
        """
        raise NotImplementedError

    def _stop(self):
        """
        stop service
        """
        raise NotImplementedError

    def _test_connection(self):
        """
        Test if the connection to the publishing service works - used during startup.
        :return: boolean. True if success
        """
        raise NotImplementedError

    def _render_message(self, messages):
        """
        takes the list of received messages (in the order they were received) and generates a message in a format
        that fits the service type

        :param messages: list of received messages. each entry is a tuple (timestamp, topic, message)
        :return: message
        """
        raise NotImplementedError

    def _send_message(self, subject, message):
        """
        sends a message with given subject to the service

        :param subject: subject as defined in config yaml - provided by task
        :param message: message to be published
        """
        raise NotImplementedError
