import logging
import collections


class LogHandler(logging.Handler):
    def __init__(self, maxlen=10000):
        logging.Handler.__init__(self)
        #super().__init__()
        self.queue = collections.deque(maxlen=maxlen)
        self.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s %(funcName)s %(message)s'
            )
        )

    def emit(self, record):
        self.queue.append(self.format(record))


logger = logging.getLogger()
logger.addHandler(LogHandler(3))
print(logger.handlers)
logger.setLevel(logging.DEBUG)


logger.debug('TEST')
logger.debug('TEST')
logger.debug('TEST')
logger.info('TEST')
logging.debug('TEST22')
logger.info('TEST')


for msg in logger.handlers[0].queue:
    print(msg)
