# bot/bot.py
#
#

""" bot package. """

import logging
import sys

from bot.base import Dotted, cdir, cfg
from bot.event import Event
from bot.handler import Handler
from bot.tasks import launch
from bot.utils import hd

## classes

class Bot(Handler):

    def __init__(self):
        super().__init__()
        self.channels = []
        self.prompt = False
        self.verbose = True

    def announce(self, txt):
        for channel in self.channels:
            self.say(channel, txt)

    def cmd(self, txt, options="", origin=""):
        if not cfg.workdir:
            cfg.workdir = hd(".bot")
            cdir(cfg.workdir)
        self.start()
        txt = self.get_aliased(txt)
        e = Event(txt)
        e.orig = repr(self)
        e.options = options
        e.origin = origin or "root@shell"
        self.dispatch(e)
        self.ready()
        return e

    def join(self):
        pass

    def raw(self, txt):
        print(txt)

    def resume(self):
        pass

    def say(self, botid, channel, txt):
        if self.verbose:
            self.raw(txt)

    def show_prompt(self):
        pass

    def work(self):
        while not self._stopped:
            event = self._queue.get()
            if not event:
                break
            self.dispatch(event)
        self.ready()
