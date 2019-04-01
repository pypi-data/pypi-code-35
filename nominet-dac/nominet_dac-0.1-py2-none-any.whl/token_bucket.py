import gevent.queue

class TokenBucket:
  def __init__(self, time_interval_in_seconds, items_per_interval, start_full=True):
    self.time_interval_in_seconds = time_interval_in_seconds
    self.items_per_interval = items_per_interval
    self.start_full = start_full
    self.running = False

  def start(self):
    items = []
    if self.start_full:
      items = [0] * self.items_per_interval
    self.bucket = gevent.queue.Queue(maxsize=self.items_per_interval, items=items)
    self.running = True
    gevent.spawn(self._start)

  def _start(self):
    while self.running:
      self.bucket.put(0)
      delay = float(self.time_interval_in_seconds)/float(self.items_per_interval)
      gevent.sleep(delay)

  def stop(self):
    self.running = False

  def wait(self):
    gevent.sleep(0)
    return self.bucket.get()

def test():
  tb = TokenBucket(60, 100)
  tb.start()
  i = 0
  while True:
    i += 1
    print(str(i) + ":" + str(tb.wait()))

if __name__ == "__main__":
  test()
