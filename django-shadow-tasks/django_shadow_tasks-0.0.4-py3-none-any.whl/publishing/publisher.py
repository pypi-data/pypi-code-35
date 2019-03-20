from functools import partial
import pika
import logging
from pika.exceptions import AMQPError

from shadow_tasks.structs import DelayedTask
from shadow_tasks.utils import get_func_full_path
from shadow_tasks.settings import shadow_settings
from shadow_tasks.schema import BrokerSchema
from shadow_tasks.registry import TaskRegistry
from shadow_tasks.mixins import ConnectionMixin

logger = logging.getLogger('project')


__all__ = ('shadow_task', 'send_shadow_task',)


class Publisher(ConnectionMixin, object):
    """Publish tasks to broker."""

    message_properties = pika.BasicProperties(
        content_type='application/json',
        delivery_mode=2,  # make message persistent
    )

    def __new__(cls, *args, **kwargs):
        """Apply singleton pattern behavior."""
        if hasattr(Publisher, '_cached_publisher'):
            return Publisher._cached_publisher

        obj = super().__new__(cls, *args, **kwargs)
        Publisher._cached_publisher = obj
        return obj

    def __init__(self):
        """Declare broker schema at a first time."""
        if getattr(self, '_schema_declared', False):
            return

        BrokerSchema().declare()
        setattr(self, '_schema_declared', True)

    def publish(self, delayed_task, repeated=False):
        """Publish task to broker."""
        try:
            self._publish(delayed_task)
        except AMQPError as e:
            if repeated:
                logger.exception(e)
            else:
                self._reopen_connection()
                self.publish(delayed_task, repeated=True)
        else:
            logger.info(f'{delayed_task} was published')

    def _publish(self, delayed_task):
        if not self._connection_operations_permitted:
            self._reopen_connection()

        self.channel.basic_publish(
            exchange=shadow_settings.EXCHANGE,
            routing_key=delayed_task.routing_key,
            body=delayed_task.to_bytes(),
            properties=self.message_properties,
        )


def shadow_task(func=None, ack_late=True):
    """Decorator for executing tasks in background."""
    if func is None:
        return partial(shadow_task, ack_late=ack_late)

    f_path = get_func_full_path(func)

    TaskRegistry.add_task(f_path)

    def delay_(*f_args, **f_kwargs):
        delayed_task = DelayedTask(f_path, f_args, f_kwargs, ack_late=ack_late)
        return Publisher().publish(delayed_task)

    func.delay = delay_ if shadow_settings.BROKER_URL else func

    return func


def send_shadow_task(f_path, *f_args, **f_kwargs):
    """Send task for shadow execution."""
    delayed_task = DelayedTask(f_path, f_args, f_kwargs)

    # TODO: add warning
    if shadow_settings.BROKER_URL:
        Publisher().publish(delayed_task)
    else:
        delayed_task()
