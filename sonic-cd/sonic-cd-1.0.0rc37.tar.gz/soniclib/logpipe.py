import logging
import threading
import os


class LogPipe(threading.Thread):

    def __init__(self, level):
        threading.Thread.__init__(self)
        self.daemon = False
        self.level = level
        self.fdRead, self.fdWrite = os.pipe()
        self.pipeReader = os.fdopen(self.fdRead)
        self.start()

    def fileno(self):
        return self.fdWrite

    def run(self):
        for line in iter(self.pipeReader.readline, ''):
            logging.log(self.level, line.strip('\n'))

        self.pipeReader.close()

    def close(self):
        os.close(self.fdWrite)

    def __exit__(self, type, value, traceback):
        self.close()

    def __enter__(self):
        return self
