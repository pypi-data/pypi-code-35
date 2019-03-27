# bot/__init__.py
#
#

""" bot package. """

__version__ = 52
__txt__ = "Framework to program bots"

## imports

import bot
import bot.handler
import logging
import sys

from bot.base import Dotted
from bot.tasks import launch
from bot.utils import hd

## classes

class Bot(bot.handler.Handler):

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
            bot.base.cdir(cfg.workdir)
        self.start()
        txt = self.get_aliased(txt)
        e = bot.event.Event(txt)
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

class Cfg(Dotted):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default = ""
        self.workdir = ""

    def __iter__(self):
        for k in self.keys():
            if k.startswith("_"):
                continue
            yield k

## defines

cfg = Cfg(_default="")
cfg.workdir = ""
cfg.logdir = ""
