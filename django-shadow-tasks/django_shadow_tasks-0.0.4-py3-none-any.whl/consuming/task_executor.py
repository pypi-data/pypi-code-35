import time
import logging

import django
from django import db

from shadow_tasks.settings import shadow_settings

logger = logging.getLogger('project')

__all__ = ('TaskExecutor',)


class TaskExecutor:
    """
    Run loop to watch and execute incoming tasks from local thread queue.
    """

    def __init__(self, tasks_limit, fetch_task, should_shutdown, on_shutdown):
        """
        Args:
            tasks_limit: how match tasks executor can handle
            fetch_task: callable method to receive task
            should_shutdown: callable shutdown flag
            on_shutdown: callback on shutdown
        """
        self.fetch_task = fetch_task
        self.tasks_limit = tasks_limit

        self.should_shutdown = should_shutdown
        self.on_shutdown = on_shutdown

        self.processed_tasks = 0
        self.sleeping_time = 0

    def run_loop(self):
        """Run loop for `self.thread_queue`."""
        self._setup()

        while self._loop_must_go_on:
            task_pack = self.fetch_task()

            if task_pack:
                self._flush_sleeping_time()
                self._execute_task(task_pack)
            else:
                self._sleep()

        self._shutdown()

    @staticmethod
    def _setup():
        django.setup(set_prefix=False)

    @property
    def _loop_must_go_on(self):
        """Check if we can handle next task."""
        if self.processed_tasks >= self.tasks_limit:
            logger.info(f'Message limit "{self.tasks_limit}" was exceeded')
            return False

        if self.sleeping_time >= shadow_settings.CONSUMER_MAX_SLEEPING_TIME:
            logger.info(
                f'Sleep timeout "{shadow_settings.CONSUMER_MAX_SLEEPING_TIME} '
                f'seconds" was exceeded')
            return False

        if self.should_shutdown():
            logger.info('Stop event was set')
            return False

        return True

    def _sleep(self):
        """Sleep while `self.thread_queue` is empty.

        Close db connection while sleeping.
        """
        time.sleep(shadow_settings.CONSUMER_SLEEP_TIMEOUT)
        self.sleeping_time += shadow_settings.CONSUMER_SLEEP_TIMEOUT

        db.connections.close_all()

    def _flush_sleeping_time(self):
        self.sleeping_time = 0

    def _execute_task(self, task_pack: tuple):
        """Execute delayed task and call callback."""
        delayed_task, on_success, on_error = task_pack

        try:
            delayed_task()
        except Exception as e:
            logger.exception(e, extra={'delayed_task': str(delayed_task)})
            on_error()
        else:
            logger.info(f'{delayed_task} was processed')
            on_success()

        finally:
            self.processed_tasks += 1

    def _shutdown(self):
        """Gracefully shutdown."""
        db.connections.close_all()
        self.on_shutdown()
