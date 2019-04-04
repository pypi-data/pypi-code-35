from pelops import mylogger
import threading
from pelops.mythreading import LoggerThread
import datetime


class Task:
    """
    A task collects messages from n topics and publishes them a specific service after x seconds and/or y messages.
    Each call of publish the list of received messages is processed and emptied. Thus, two consecutive calls of
    publish will produce two different messages (or two empties with an empty list). To ensure this behavior, a lock
    is used to block access to the list.

    config yaml structure:
      - name: collection
        service: stdout  # [email, stdout, ...] one of the services
        subject: sending collected messages  # subject for message
        every-nth-message: 10  # collect this amount of messages before publishing them. 0 for never
        every-nth-second: 10  # wait this time before publishing all messages that are waiting. 0 for never
        topics-sub:
            - /test/a
            - /test/b
            - /test/c
    """

    _config = None  # config yaml structure
    _mqtt_client = None  # mqtt client instance
    _logger = None  # logger instance

    _topics_sub = None  # list of subscribed topics
    _message_handler = None  # list of the handlers for the subscribed topics

    _service = None  # instance of the service to be used
    _subject = None  # subject for each publish message
    name = None  # name of the service

    _every_nth_message = None  # collect this amount of messages before publishing them. 0 for never
    _use_every_message = None  # true if _every_nth_message > 0

    _every_nth_second = None  # wait this time before publishing all messages that are waiting. 0 for never
    _use_every_second = None  # true if _use_every_second > 0
    _loop_thread = None  # thread for timer loop
    _stop_loop = None  # event signals that timer loop should stop

    _message_list = None  # list of unprocessed messages received from all topics
    _lock_list = None  # locks the message list (mutual exclusive access for renderer and handler)

    def __init__(self, config, services, mqtt_client, logger):
        """
        Constructor

        :param config: config yaml structure
        :param services: list of services created by servicefactory
        :param mqtt_client: mqtt client instances
        :param logger: logger instance
        """
        self._config = config
        self.name = self._config["name"]
        self._mqtt_client = mqtt_client
        self._logger = mylogger.get_child(logger, __name__ + "." + self.name)

        self._logger.info("Task.__init__ - start")
        self._logger.debug("Task.__init__ - config: {}".format(self._config))

        self._subject = self._config["subject"]
        self._topics_sub = self._config["topics-sub"]
        self._service = services[self._config["service"].lower()]

        self._every_nth_message = self._config["every-nth-message"]
        if self._every_nth_message == 0:
            self._use_every_message = False
        else:
            self._use_every_message = True

        self._every_nth_second = self._config["every-nth-second"]
        if self._every_nth_second == 0:
            self._use_every_second = False
        else:
            self._use_every_second = True
        self._loop_thread = LoggerThread(target=self._loop, name="task_{}".format(self.name), logger=self._logger)
        self._stop_loop = threading.Event()
        self._stop_loop.set()

        self._message_handler = {}
        for topic in self._topics_sub:
            self._message_handler[topic] = self._create_handler(topic)

        self._message_list = []
        self._lock_list = threading.Lock()

        self._logger.info("Task.__init__ - finished")

    def _create_handler(self, handler_topic):
        """
        For each sub topic a handler is created that adds incoming messages to the list of messages that are processed
        into an outgoing message.
        """
        def _handler(message):
            timestamp = datetime.datetime.now()
            entry = (timestamp, handler_topic, message)
            self._logger.info("Task._handler.'{}' - received message".format(handler_topic))
            self._logger.debug("Task._handler.'{}' - {}".format(handler_topic, entry))
            with self._lock_list:
                self._logger.debug("Task._handler.'{}' - lock acquired".format(handler_topic))
                self._message_list.append(entry)
            self._logger.debug("Task._handler.'{}' - lock released".format(handler_topic))
            self._logger.debug("Task._handler.'{}' - added message to list".format(handler_topic))
            self._handler_post_processor()

        self._logger.debug("Task._create_handler - added handler {} for topic {}.".format(_handler, handler_topic))
        return _handler

    def _handler_post_processor(self):
        """
        after each added message to the list, the system checks if list size is larger than _every_nth_message. if
        yes, publish message is called.
        """
        if self._use_every_message and len(self._message_list) >= self._every_nth_message:
            self._logger.info("Task._handler_post_processer - message_list size: {}.".format(len(self._message_list)))
            self._publish()

    def _loop(self):
        """
        if _every_nth_second is set, this method waits n seconds and publishes all messages in the list.
        """
        self._logger.info("Task._loop - start loop")
        while not self._stop_loop.is_set():
            self._logger.info("Task._loop - wait for {} seconds.".format(self._every_nth_second))
            self._stop_loop.wait(self._every_nth_second)
            if self._stop_loop.is_set():
                continue
            self._logger.info("Task._loop - sending messages")
            self._publish()

    def _publish(self):
        """
        A copy of the received messages is given to the service handler and published. The stored messages are cleared
        afterwards. The list is protected by _lock_list during processing.
        """
        self._logger.info("Task._publish - start")
        with self._lock_list:
            self._logger.debug("Task._publish - lock acquired")
            messages = self._message_list.copy()
            self._logger.debug("Task._publish - copied {} messages.".format(len(messages)))
            self._message_list.clear()
        self._logger.debug("Task._publish - lock released")
        self._service.publish(self._subject, messages)
        self._logger.info("Task._publish - finished")

    def start(self):
        """
        Starts the task (if timer is used, a thread with _loop is started) and subscribes to all sub topics.
        """
        self._logger.info("Task.start - starting")
        if self._use_every_second:
            self._logger.info("Task.start - start loop")
            self._stop_loop.clear()
            self._loop_thread.start()
        self._logger.info("Task.start - register {} topics".format(len(self._message_handler.items())))
        for topic, handler in self._message_handler.items():
            self._logger.debug("Task.start - subscribing to topic {} the handler {}".format(topic, handler))
            self._mqtt_client.subscribe(topic, handler)
        self._logger.info("Task.start - finished")

    def stop(self):
        """
        Stops the task (and the timer thread) and unsubscribes from the topics.
        """
        self._logger.info("Task.stop - stopping")
        self._logger.info("Task.start - unregister {} topics".format(len(self._message_handler.items())))
        for topic, handler in self._message_handler.items():
            self._logger.debug("Task.start - unsubscribing from topic {} the handler {}".format(topic, handler))
            self._mqtt_client.unsubscribe(topic, handler)
        if self._use_every_second:
            self._logger.info("Task.start - stop loop")
            self._stop_loop.set()
            self._loop_thread.join()
        self._logger.info("Task.stop - finished")
