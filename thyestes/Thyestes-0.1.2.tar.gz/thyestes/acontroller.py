import threading
import pelops.logging.mylogger


class AController:
    """...

    config:
        name: eggtimer  # unique name for timer
        topic-sub: /test/1/event  # topics to be subscribed to
        topic-command: start  # message that initiates the timer. optional - if no-entry or None as value every message will trigger timer
        topic-pub: /test/1/timer  # topic to publish the timer event to
        timer-message: timer  # message to be published when a timer event happens
        timer-value: 30  # timeout in seconds
    """

    _timer_value = -1  # poll time in seconds
    _stop_timer = None  # threading.Event to signal the poll loop to stop immediately.
    _timer_stopped = None

    _config = False
    _logger = False  # print debugging information if set to yes.
    _mqtt_client = False  # mqtt client instance

    def __init__(self, config, mqtt_client, logger):
        self._config = config
        self._logger = pelops.logging.mylogger.get_child(logger, self._config["name"])
        self._mqtt_client = mqtt_client

        self._logger.info("AController.__init__ - starting constructor")
        self._logger.debug("AController.__init__ - config: '{}'".format(self._config))

        self._timer_value = float(self._config["timer-value"])
        self._topic_sub = self._config["topic-sub"]
        try:
            self._topic_command = self._config["topic-command"]
            if not self._topic_command or len(self._topic_command) == 0:
                self._topic_command = None
        except KeyError:
            self._topic_command = None
        self._topic_pub = self._config["topic-pub"]
        self._timer_message = self._config["timer-message"]

        self._stop_timer = threading.Event()
        self._stop_timer.set()

    def _message_handler(self, value):
        value = value.decode()
        self._logger.info("_message_handler - received message")
        self._logger.debug("_message_handler - message content: '{}'".format(value))
        if not self._topic_command or self._topic_command == value:
            self._logger.info("_message_handler - processing message")
            self._update_timer()
        else:
            self._logger.info("_message_handler - skipping message")
            self._logger.debug("_message_handler - content of message is not equivalent to expected value "
                               "('{}')".format(self._topic_command))

    def _update_timer(self):
        raise NotImplementedError

    def start(self):
        self._logger.info("AController.start - starting controller.")
        self._stop_timer.clear()
        self._start()
        self._mqtt_client.subscribe(self._topic_sub, self._message_handler)
        self._logger.info("AController.start - controller started.")

    def _start(self):
        raise NotImplementedError

    def _publish_timer_message(self):
        self._logger.info("AController._publish_timer_message - publishing '{}' to topic '{}'.".
                          format(self._timer_message, self._topic_pub))
        self._mqtt_client.publish(self._topic_pub, self._timer_message)

    def stop(self):
        self._logger.info("AController.stop - stopping controller.")
        self._mqtt_client.unsubscribe(self._topic_sub, self._message_handler)
        self._stop_timer.set()
        self._stop()
        self._logger.info("AController.stop - controller stopped.")

    def _stop(self):
        raise NotImplementedError

