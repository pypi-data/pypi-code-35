import time

from shadow_tasks.utils import get_broker_connection

__all__ = ('ConnectionMixin',)


class ConnectionMixin:

    connection = None
    channel = None

    def _reopen_connection(self):
        """Переинициализирует соединение."""
        self._stop_connection()
        self._setup_connection()

    def _setup_connection(self):
        """Начинает работу с RabbitMQ по приему сообщений.

        Если на старте не получается установить соединение - consumer упадет.
        За такими ситуациями должен следить клиентский код.
        """
        self.connection = get_broker_connection()
        self.channel = self.connection.channel()

    def _stop_connection(self):
        """Останавливает соединение."""
        self._close_channel()
        self._close_connection()

    def _close_channel(self):
        """Gracefully close channel."""
        self._gracefully_close_communication('channel')

    def _close_connection(self):
        """Gracefully close connection."""
        self._gracefully_close_communication('connection')

    def _gracefully_close_communication(self, communication_type):
        """Gracefully close channel or connection."""

        assert communication_type in ('channel', 'connection',), (
            f'Invalid communication_type {communication_type}')

        communication = getattr(self, communication_type)

        if not communication:
            return

        if communication.is_closed:
            setattr(self, communication_type, None)
            return

        if not communication.is_closing:
            communication.close()

        while communication.is_closing:
            time.sleep(0.25)

        setattr(self, communication_type, None)

    @property
    def _connection_operations_permitted(self):
        """Проверяет, можно ли выполнять операцию."""
        return bool(
            self.connection and self.connection.is_open and
            self.channel and self.channel.is_open
        )
