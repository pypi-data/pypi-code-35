import logging
from threading import Thread
from queue import Empty
import backoff

from hawkei.processor.batch import Batch
from hawkei.request import create, ApiError
from hawkei.resources.batch import Batch as BatchResource

_INTERVAL = 3
_MAX_RETRIES = 10

class Worker(Thread):
    logger = logging.getLogger('hawkei')

    def __init__(self, queue):
        Thread.__init__(self)

        self.queue = queue
        self.daemon = True
        self.running = True
        self.batch = Batch()

    def run(self):
        self.logger.debug('worker is running ...')

        while self.running:
            try:
                message = self.queue.get(block=True, timeout=_INTERVAL)
                self.batch.add(message)
                if self.batch.is_full():
                    self.send_batch()

            except Empty:
                if not self.batch.is_empty(): self.send_batch()
                continue

        self.logger.debug('worker stopped')

    def stop(self):
        self.running = False

    def send_batch(self):

        def check_exception(error):
            if isinstance(error, ApiError):
                return error.status_code in [401, 404, 422]
            return False

        @backoff.on_exception(backoff.expo, Exception, max_tries=_MAX_RETRIES, giveup=check_exception)
        def send():
            create(BatchResource, {'data': self.batch.messages})

        self.logger.debug('send batch with: %d messages', len(self.batch.messages))
        try:
            send()
        except Exception as ex: # pylint: disable=W0703
            self.logger.error(ex)
        finally:
            self.queue.task_done()
            self.batch = Batch()
