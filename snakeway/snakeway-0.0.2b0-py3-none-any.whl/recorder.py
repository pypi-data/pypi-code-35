from queue import Queue
from threading import Thread

from snakeway.stats import Stats


class Recorder(Thread):
    def __init__(self, q: Queue, stats: Stats) -> None:
        super().__init__()
        self.q = q
        self.daemon = True
        self.stats = stats

    def run(self):
        while True:
            data = self.q.get()
            self.stats.put(data)
