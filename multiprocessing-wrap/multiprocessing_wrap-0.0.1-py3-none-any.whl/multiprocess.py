"""This module is a light wrapper for the `multiprocessing` module
"""
import multiprocessing
import traceback
import dill
from tqdm import tqdm

MANAGER = multiprocessing.Manager()


class MultiprocessException(Exception):
  """Error thrown by this module"""


class Multiprocess:
  """This class offers the functionality of multiprocessing,
  with inbuilt error support and a simple interface"""

  def __init__(self, show_loading_bar=True):
    self.pool = multiprocessing.Pool()
    self.jobs = []
    self.show_loading_bar = show_loading_bar
    self.err_q = Queue()
    self.alive = True

  def _reset(self):
    while not self.err_q.empty():
      self.err_q.pop()
    self.jobs = []

  def add_tasks(self, function, arr_of_args):
    """add tasks to be done"""
    if not self.alive:
      raise MultiprocessException("CLOSED, refusing to add tasks")
    arr = [dill.dumps((function, self.err_q) + (args)) for args in arr_of_args]
    self.jobs += arr

  def do_tasks(self, called_from_close=False):
    """Block the thread and complete the tasks"""
    if not self.alive:
      if called_from_close:
        return
      raise MultiprocessException('CLOSED, refusing to do tasks')
    pbar = None
    job_count = len(self.jobs)
    if job_count == 0:
      return
    if self.show_loading_bar:
      pbar = tqdm(total=job_count)

    if not self.show_loading_bar:
      self.pool.imap_unordered(my_worker, self.jobs)
    else:
      for _ in enumerate(self.pool.imap_unordered(my_worker, self.jobs)):
        self._check_for_exceptions()
        pbar.update(1)

    # Raise exceptions, if there were any
    self._check_for_exceptions()
    if pbar:
      pbar.close()
    self._reset()

  def _check_for_exceptions(self):
    if not self.err_q.empty():
      exceptions = []
      while not self.err_q.empty():
        exceptions.append(self.err_q.pop())
      self._reset()
      self.close()
      raise MultiprocessException(
          '%s errors occurred:\n' % len(exceptions) +
          "\n".join(['ERROR: ' + str(e) for e in exceptions]))

  def close(self):
    self.do_tasks(True)
    self.alive = False
    self.pool.close()


def my_worker(args):
  args = dill.loads(args)
  fn = args[0]
  err_q = args[1]
  rem_args = args[2:]
  try:
    fn(*rem_args)
  except Exception:
    err_q.push('Error in function call "%s(%s)"\n%s' %
               (fn.__name__, rem_args, traceback.format_exc()))


class Queue:
  """A lightweight wrapper for multiprocess.manager.Queue()"""

  def __init__(self):
    self.q = MANAGER.Queue()
    #for method in dir(self.q):
    #  if method[0] != '_':
    #    setattr(self, method, getattr(self.q, method]))

  def get(self):
    return self.q.get()

  def put(self, v):
    self.q.put(v)

  def pop(self):
    return self.get()

  def push(self, v):
    self.q.put(v)

  def empty(self):
    return self.q.empty()

  def qsize(self):
    return self.q.qsize()
