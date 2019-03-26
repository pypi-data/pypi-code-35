# bot/handler.py
#
#

""" event handler. """

import logging
import queue
import sys
import time
import threading

import bot
import bot.loader
import bot.tasks
import bot.utils

from bot.tasks import launch
from bot.utils import get_exception, get_name

## exceptions

class ENOTIMPLEMENTED(Exception):
    pass

## classes

class Handler(bot.loader.Loader):

    def __init__(self):
        super().__init__()
        self._curevent = None
        self._events = []
        self._queue = queue.Queue()
        self._ready = threading.Event()
        self._stopped = False
        self._threaded = True
        self._thrs = []

    def collect(self):
        for thr in self._thrs:
            thr.join()
        while 1:
            try:
                event = self._events.pop()
                time.sleep(0.001)
            except IndexError:
                continue
            event.wait()
            try:
                self._events.remove(event)
            except ValueError:
                pass

    def dispatch(self, event):
        event._func = self.get_cmd(event)
        if event._func:
            logging.info("dispatch %s %s" % (event.origin, get_name(event._func)))
            try:
                event._func(event)
            except Exception:
                event.trace = get_exception()
            event.show(self)
        event.ready()

    def get_cmd(self, event):
        return self.get_handler(event.cmd)

    def get_event(self):
        return self._queue.get()

    def loop(self):
        while not self._stopped:
            try:
                event = self.get_event()
            except EOFError:
                break
            if not event:
                continue
            if self._threaded:
                thr = launch(self.dispatch, event)
                event._thrs.append(thr)
            else:
                self.dispatch(event)
        self.ready()

    def put(self, event):
        self._queue.put_nowait(event)

    def ready(self):
        self._ready.set()

    def start(self):
        launch(self.loop)

    def stop(self):
        self._stopped = True
        self._queue.put(None)

    def wait(self):
        return self._ready.wait()

    def work(self):
        while not self._stopped:
            event = self._queue.get()
            if not event:
                break
            self.dispatch(event)
        self.ready()
