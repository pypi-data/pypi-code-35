import logging
import atexit
import queue

from hawkei.processor.worker import Worker

_MAX_QUEUE_SIZE = 10000

class Async():
    logger = logging.getLogger('hawkei')

    def __init__(self):
        self.queue = queue.Queue(_MAX_QUEUE_SIZE)
        self.worker = Worker(self.queue)

        atexit.register(self.shutdown)
        self.worker.start()

    def enqueue(self, message):
        try:
            self.queue.put(message, block=False)
            return True

        except queue.Full:
            return False

    def flush(self):
        self.logger.debug('flush')
        self.queue.join()

    def shutdown(self):
        self.logger.debug('start stopping worker ...')
        self.worker.stop()
        self.flush()
        try:
            self.worker.join()
        except RuntimeError:
            pass
