import abc
import threading
import time

from amqpstorm import AMQPError, Connection, Message
from minty import Base
from minty.cqrs import CQRS


class BaseConsumer(abc.ABC, Base):
    def __init__(
        self,
        queue: str,
        routing_keys: str,
        exchange: str,
        cqrs: CQRS,
        dead_letter_config: dict,
        qos_prefetch_count: int = 1,
    ):
        self.cqrs = cqrs
        self.queue = queue
        self.exchange = exchange
        self.routing_keys = routing_keys
        self.channel = None
        self.active = False
        self.qos_prefetch_count = qos_prefetch_count
        self.dead_letter_exchange_config = dead_letter_config

    def start(self, connection: Connection, ready: threading.Event):
        """Initialize channel, declare queue and start consuming.

        This method should not be overloaded in subclassed consumers.

        :param connection: Connection to rabbitmq
        :type connection: Connection
        :param ready: signals if initialization is done
        :type ready: threading.Event
        """
        self.channel = None
        try:
            self.channel = connection.channel(rpc_timeout=10)
            self.active = True
            self.channel.basic.qos(self.qos_prefetch_count)
            queue_args = {}

            if self.dead_letter_exchange_config:
                dlx = self.dead_letter_exchange_config
                dlx_args = {
                    "x-dead-letter-exchange": self.exchange,
                    "x-message-ttl": dlx["retry_time_ms"],
                }
                self._declare_exchange_and_queue(
                    exchange=dlx["exchange"],
                    queue=dlx["queue"],
                    queue_args=dlx_args,
                )
                queue_args = {"x-dead-letter-exchange": dlx["exchange"]}

            self._declare_exchange_and_queue(
                exchange=self.exchange, queue=self.queue, queue_args=queue_args
            )
            self.channel.basic.consume(self, self.queue, no_ack=False)

            ready.set()

            # start_consuming() blocks indefinitely or until channel is closed.
            self.channel.start_consuming()

            self.channel.close()
        except AMQPError as err:
            self.logger.warning(err)
            time.sleep(1)
        finally:
            self.active = False

    def _declare_exchange_and_queue(
        self, exchange: str, queue: str, queue_args: dict
    ):
        """Declare exchange, queue and bind routing keys.

        :param exchange: exchange name
        :type exchange: str
        :param queue: queue name
        :type queue: str
        :param queue_args: queue arguments
        :type queue_args: dict
        """
        self._declare_exchange(name=exchange)
        self._declare_queue(name=queue, arguments=queue_args)
        self._bind_queue_to_routing_keys(queue=queue, exchange=exchange)

    def _declare_exchange(self, name: str):
        """Declare Exchange, ignore if exists.

        :param name: exchagne name
        :type name: str
        """
        self.channel.exchange.declare(
            exchange=name,
            exchange_type="topic",
            durable=True,
            auto_delete=False,
        )

    def _declare_queue(self, name: str, arguments: dict):
        """Declare queue, ignore if exists.

        :param name: queue name
        :type name: str
        :param arguments: queue arguments
        :type arguments: dict
        """
        self.channel.queue.declare(
            queue=name, durable=True, arguments=arguments
        )

    def _bind_queue_to_routing_keys(self, queue: str, exchange: str):
        """Loop over `routing_keys` and bind queue."""
        for routing_key in self.routing_keys:
            self.channel.queue.bind(
                queue=queue, exchange=exchange, routing_key=routing_key
            )

    def stop(self):
        """Stop consumer and close channel."""
        if self.channel:
            self.channel.close()

    @abc.abstractmethod
    def __call__(self, message: Message):
        """Process received message in sublassed consumer.

        Subclassed consumers should implement the message processing logic when
        overloading this method. This should result in a call to
        `message.ack()` on success and a call to `message.nack()` on failure.

        :param message: received amqp message
        :type message: Message
        """
        print(f"received message: {message.body}")
        message.ack()
