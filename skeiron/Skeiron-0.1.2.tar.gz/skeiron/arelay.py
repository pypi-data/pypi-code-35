import pelops.mylogger


class ARelay:
    _config = None
    _mqtt_client = None
    _logger = None

    name = None

    _replace_message_flag = None
    _replace_message = None

    _topics_pub = None
    _topics_sub = None

    def __init__(self, config, mqtt_client, logger):
        self._config = config
        self._mqtt_client = mqtt_client
        self._logger = pelops.mylogger.get_child(logger, self._config["name"])

        self._logger.info("ARelay.__init__ - initializing")
        self._logger.debug("ARelay.__init__ - config: '{}'.".format(self._config))

        self.name = self._config["name"]
        try:
            self._replace_message = self._config["replace-message"]
            self._replace_message_flag = True
        except KeyError:
            self._replace_message_flag = False

        self._topics_pub = []
        self._topics_sub = []

    def _message_handler(self, value):
        self._logger.info("ARelay._message_handler - relaying message")
        if self._replace_message_flag:
            value = self._replace_message
            self._logger.debug("ARelay._message_handler - using replace message")
        for topic in self._topics_pub:
            self._logger.debug("ARelay._message_handler - publishing message '{}' to topic '{}'.".format(value, topic))
            self._mqtt_client.publish(topic, value)

    def start(self):
        self._logger.info("ARelay.start - subscribing topics")
        for topic in self._topics_sub:
            self._logger.debug("ARelay.start - subscribing topic '{}'.".format(topic))
            self._mqtt_client.subscribe(topic, self._message_handler)

    def stop(self):
        self._logger.info("ARelay.stop - unsubscribing topics")
        for topic in self._topics_sub:
            self._logger.debug("ARelay.stop - unsubscribing topic '{}'.".format(topic))
            self._mqtt_client.unsubscribe(topic, self._message_handler)
