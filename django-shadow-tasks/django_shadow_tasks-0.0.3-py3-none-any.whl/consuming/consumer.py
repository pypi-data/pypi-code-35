import logging
from functools import partial

from pika.exceptions import AMQPError

from shadow_tasks.utils import get_broker_connection
from shadow_tasks.structs import DelayedTask

logger = logging.getLogger('project')

__all__ = ('get_consumer',)


def get_handle_broker_incoming_message(con, send_task_to_execute):
    """Wrap `handle_broker_incoming_message` to pass `con` and
    `send_to_execute` params into."""

    def handle_broker_incoming_message(ch, method, properties, body):
        """Dispatch RabbitMQ to `DelayedTask` and pass to `thread_queue`
        for execution."""
        try:
            delayed_task = DelayedTask.from_bytes(body)

        except Exception as e:
            logger.exception(e)
            ch.basic_nack(method.delivery_tag, requeue=False)
            return

        ack_ = partial(ch.basic_ack, method.delivery_tag)
        on_success = partial(con.add_callback_threadsafe, ack_)

        nack_ = partial(ch.basic_nack, method.delivery_tag, requeue=False)
        on_error = partial(con.add_callback_threadsafe, nack_)

        task_pack = (
            delayed_task,
            on_success,
            on_error if delayed_task.ack_late else on_success,
        )
        send_task_to_execute(task_pack)

    return handle_broker_incoming_message


def get_consumer(queue_name, send_task_to_execute=None, on_shutdown=None):
    """Run consumer as a coroutine."""
    connection = get_broker_connection()
    channel = connection.channel()

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        get_handle_broker_incoming_message(connection, send_task_to_execute),
        queue=queue_name,
    )

    # Return connection and channel into main program and wait until
    # additional thread will start
    yield connection, channel

    try:
        channel.start_consuming()

    except AMQPError as e:
        logger.exception(e)

    finally:
        logger.info('Stop consumer')
        on_shutdown()
