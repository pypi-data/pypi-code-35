import logging
from pika.exceptions import AMQPError
from shadow_tasks.settings import shadow_settings
from shadow_tasks.mixins import ConnectionMixin

logger = logging.getLogger('project')

__all__ = ('BrokerSchema',)


class BrokerSchema(ConnectionMixin, object):
    """Builds exchanges and queues."""

    def declare(self):
        """Создает при необходиомсти exchange-и и queues в RabbitMQ."""
        try:
            self._declare_broker_routes_schema()
        except AMQPError as e:
            logger.exception(e)

    def _declare_broker_routes_schema(self):
        self._setup_connection()
        self._setup_exchanges()
        self._setup_queues()
        self._stop_connection()

    def _setup_exchanges(self):
        # Объявляем кастомный exchange
        self.channel.exchange_declare(
            exchange=shadow_settings.EXCHANGE,
            exchange_type='direct',
            durable=True,
        )

        # Объявляем DLX (dead letter exchange)
        self.channel.exchange_declare(
            exchange=shadow_settings.DLX_EXCHANGE,
            exchange_type='fanout',
            durable=True,
        )

    def _setup_queues(self):
        """Создает очереди в RabbitMQ, соотвествующие ключам маршрутизации
        из `self.router`.

        Настраивает также маршрутизацию из `self.exchange` в эти очереди.
        """
        queues = (
            set(shadow_settings.QUEUE_TASKS_MAP.keys()) |
            {shadow_settings.DEFAULT_QUEUE}
        )
        for queue in queues:
            dlx_queue_name = (
                f'_{queue}_dlx' if shadow_settings.DLX_PER_QUEUE
                else shadow_settings.DLX_DEFAULT_QUEUE_NAME
            )

            self.channel.queue_declare(
                queue=queue,
                durable=True,
                arguments={
                    'x-dead-letter-exchange': dlx_queue_name,
                },
            )
            self.channel.queue_bind(
                exchange=shadow_settings.EXCHANGE,
                queue=queue,
                routing_key=queue,
            )

            if shadow_settings.DLX_PER_QUEUE:
                self._declare_dlx_queue(dlx_queue_name)

        if not shadow_settings.DLX_PER_QUEUE:
            self._declare_dlx_queue(shadow_settings.DLX_DEFAULT_QUEUE_NAME)

    def _declare_dlx_queue(self, dlx_queue_name):
        # Declare dead letter exchange
        self.channel.queue_declare(
            queue=dlx_queue_name,
            durable=True,
            arguments={
                'x-message-ttl': shadow_settings.DLX_TIMEOUT * 1000,
                # Return from dlx to main exchange
                'x-dead-letter-exchange': shadow_settings.EXCHANGE,
            }
        )
        self.channel.queue_bind(
            exchange=shadow_settings.DLX_EXCHANGE,
            queue=dlx_queue_name,
        )
