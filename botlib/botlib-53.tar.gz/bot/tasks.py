# bot/tasks.py
#
#

""" bot threads. """

import logging
import queue
import threading
import time

import bot
import bot.base
import bot.utils

from bot.base import Dotted, starttime
from bot.utils import elapsed, get_exception, get_name

## classes

class Task(threading.Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(None, self.run, "", [], kwargs, daemon=True)
        self._queue = queue.Queue()
        self._func = None
        self._ready = threading.Event()
        self._result = None
        self._stopped = False

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def put(self, func, args, kwargs):
        self._queue.put((func, args, kwargs))

    def run(self):
        (func, args, kwargs) = self._queue.get()
        try:
            e = args[0]
            txt = e.cmd
        except (IndexError, AttributeError):
            txt = get_name(func)
        self.setName(txt)
        try:
            self._result = func(*args, **kwargs)
        except Exception as ex:
            txt = get_exception()
            logging.error(txt)
        self._ready.set()
        return self._result

    def join(self, timeout=None):
        super().join(timeout)
        return self._result

    def stop(self):
        self._stopped = True
        self._queue.put(None)

    def wait(self):
        self._ready.wait()

class Tasks(Dotted):

    def __init__(self):
        super().__init__()
        self._queue = queue.Queue()
        self._result = []
        self._stopped = False
        self._thrs = []
        self.state = Dotted()
        self.state.maxtasks = 1
        self.state.nrtasks = 0

    def loop(self):
        while not self._stopped:
            func, args, kwargs = self._queue.get()
            if self.state.nrtasks < self.state.maxtasks:
                thr = launch(func, *args, **kwargs)
                self._thrs.append(thr)
                self.state.nrtasks += 1
            
    def reaper(self):
        while not self._stopped:
           for thr in self._thrs:
               thr.join()
               self.state.nrtasks -= 1
               self._thrs.remove(thr)
           time.sleep(0.001)

    def put(self, func, *args, **kwargs):
        if self.state.nrtasks <= self.state.maxtasks:
            self._queue.put((func, args, kwargs))
        else:
            self._queue.put_nowait((func, args, kwargs))

    def start(self):
        launch(self.loop, daemon=True)
        launch(self.reaper, daemon=True)

## functions

def kill(thrname=""):
    for task in running(thrname):
        if "cancel" in dir(task):
            task.cancel()
        if "exit" in dir(task):
            task.exit()
        if "stop" in dir(task):
            task.stop()

def launch(func, *args, **kwargs):
    t = Task()
    t.start()
    t.put(func, args, kwargs)
    return t

def running(tname=""):
    for task in threading.enumerate():
        n = str(task)
        if n.startswith("<_"):
            continue
        if tname and tname.upper() not in n.upper():
            continue
        yield task

## commands

def stop(event):
    if not event.args:
        event.reply("stop <threadname>")
        return
    name = event.args[0]
    kill(name)
    event.reply("ok %s" % name)
