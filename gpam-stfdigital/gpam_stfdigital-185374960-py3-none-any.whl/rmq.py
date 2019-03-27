import pika
import time
from pika.exceptions import ConnectionClosed


class RMQConnection:
    """Config connection with rabbit rmq"""

    WAIT_SECONDS_FOR_CONNECTION = 60

    def __init__(self, host, routing_key, exchange_name):

        parameters = pika.ConnectionParameters(host)
        self._connection = self._set_up_connection(parameters)
        self._channel = self._connection.channel()

        self._channel.exchange_declare(exchange=exchange_name,
                                       exchange_type='topic')

        queue = self._channel.queue_declare(exclusive=True)

        self._queue_name = queue.method.queue

        self._channel.queue_bind(exchange=exchange_name,
                                 queue=self._queue_name,
                                 routing_key=routing_key)

    def get_consume(self):
        return self._channel.consume(self._queue_name)

    def return_ack(self, method):
        """
        Return delivery tag
        """
        self._channel.basic_ack(method.delivery_tag)

    def _set_up_connection(self, parameters):
        """
        Return a Blocking connection
        """

        conn = None

        for _ in range(self.WAIT_SECONDS_FOR_CONNECTION):

            try:
                conn = pika.BlockingConnection(parameters)
            except ConnectionClosed:
                time.sleep(1)

        return conn
