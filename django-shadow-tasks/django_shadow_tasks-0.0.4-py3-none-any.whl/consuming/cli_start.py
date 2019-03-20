import sys
import queue
import threading
import signal
import logging

from functools import partial

from django.conf import settings
from django.utils.log import configure_logging

from shadow_tasks.settings import shadow_settings
from shadow_tasks.consuming.task_executor import TaskExecutor
from shadow_tasks.consuming.consumer import get_consumer
from shadow_tasks.schema import BrokerSchema

configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)

logger = logging.getLogger('project')


class StopEvent:
    is_set = False

    @classmethod
    def stop(cls):
        cls.is_set = True

    @classmethod
    def is_stopped(cls):
        return cls.is_set


def fetch_task_to_execute(threading_queue):
    """Wraps fetching task from threading_queue."""
    task_pack = None

    try:
        task_pack = threading_queue.get(block=False)
    except queue.Empty:
        pass

    return task_pack


def start_consuming(rabbit_queue_name, tasks_limit):
    """Run fetching and executing tasks from RabbitMQ.

    Task executor is running in separate thread.
    """
    threading_queue = queue.Queue(maxsize=1)

    consumer = get_consumer(
        rabbit_queue_name,
        send_task_to_execute=threading_queue.put,
        on_shutdown=StopEvent.stop,
    )
    con, ch = next(consumer)

    executor = TaskExecutor(
        tasks_limit,
        fetch_task=partial(fetch_task_to_execute, threading_queue),
        should_shutdown=StopEvent.is_stopped,
        on_shutdown=partial(con.add_callback_threadsafe, ch.stop_consuming),
    )

    thread = threading.Thread(target=executor.run_loop)
    thread.start()

    try:
        next(consumer)

    except StopIteration:
        # Normal consumer shut down
        pass

    except Exception as e:
        logger.exception(e)

    finally:
        StopEvent.stop()
        logger.info('Wait for thread completed')
        thread.join()


def service_shutdown(signum, frame):
    logger.info(f'Caught signal {signum}')
    StopEvent.is_set = True


def execute_from_command_line(argv=None):
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    argv = argv or sys.argv[:]

    assert len(argv) == 3

    _, queue_name_arg, task_limit_arg = argv

    logger.info(
        f'Start consumer for "{queue_name_arg}" queue. '
        f'Max sleeping timeout "{shadow_settings.CONSUMER_MAX_SLEEPING_TIME}"'
    )

    BrokerSchema().declare()

    start_consuming(queue_name_arg, int(task_limit_arg))
