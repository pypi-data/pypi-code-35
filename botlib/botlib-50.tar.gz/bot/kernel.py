# bot/kernel.py
#
#

""" main loop. """

import logging
import os
import sys
import threading
import time

import bot
import bot.base
import bot.bot
import bot.event
import bot.fleet
import bot.poller
import bot.shell
import bot.utils

from bot.base import basic_types, cdir, cfg, get_cls, get_clsfromstr, get_type, __version__
from bot.shell import daemon, level, opts, parse_cli, reset, startup, set_completer
from bot.tasks import launch
from bot.utils import get_exception, get_name, hd

## defines

defaults = bot.base.Dotted()
defaults.exclude = ""
defaults.logdir = ""
defaults.modules = ""
defaults.name = "bot"
defaults.options = ""
defaults.shell = False
defaults.usage = ""
defaults.version = __version__
defaults.wait = True
defaults.workdir = cfg.workdir

## classes

class Cfg(bot.base.Dotted):

    _default = ""

class Kernel(bot.fleet.Fleet, bot.poller.Poller, bot.store.Store):

    """ core module providing boot code. """

    def __init__(self):
        super().__init__()
        self._in = sys.stdin    
        self._out = sys.stdout
        self._err = sys.stderr
        self.cfg = Cfg(defaults)
        self.prompt = False
        self.verbose = False
        self.loaded = []

    def cmd(self, txt, options="", origin=""):
        if not cfg.workdir:
            cfg.workdir = hd(".%s" % cfg.name)
            cdir(cfg.workdir)
        super().start()
        txt = self.get_aliased(txt)
        e = bot.event.Event(txt)
        e.orig = repr(self)
        e.options = options
        e.origin = origin or "root@shell"
        self.dispatch(e)
        self.ready()
        return e

    def say(self, orig, channel, txt):
        if self.verbose:
            self._out.write(str(txt))
            self._out.write("\n")
            self._out.flush()
        
    def start(self, name, bots=[], modules="",  version=__version__, workdir=""):
        """ start the program. """
        parse_cli(name, opts, "%s [options]" % name, version, workdir or hd(".%s" % name.lower()))
        level(cfg.level)
        if cfg.background:
            daemon()
        logging.warn("%s started at %s" % (name.upper(), time.ctime(time.time())))
        prev = Cfg(self.cfg)
        self.cfg.update(cfg)
        if prev != self.cfg:
            self.cfg.save()
        else:
            last = self.last(get_type(self.cfg))
            if last:
                self.cfg.update(last)
        if type(bots) != list:
            bots = [bots,]
        for bot in bots:
            bot.start()
            self.add(bot)
            #if "_in" in dir(bot):
            #    self.register_fd(bot._in)
        res = []
        thrs = []
        names = self.cfg.modules + "," + modules
        mods = [x for x in names.split(",") if x]
        for m in mods:
            try:
                res.extend(self.walk(m))
            except ModuleNotFoundError:
                pass
        for mod in res:
            if "init" in dir(mod):
                thr = mod.init()
                if not thr:
                    continue
                if type(thr) == list:
                    for t in thr:
                        t.join()
                else:
                    thr.join()
        logging.info("cmds are %s" % ",".join(self.names.keys()))
        set_completer(self.names.keys())
        super().start()
        if self.cfg.shell:
            for bot in bots:
                bot.show_prompt()

    def unload(self, name):
        """ unload a module from all bots in the fleet. """
        for bot in self.bots:
            bot.unload(name)

    def wait(self):
        if not self.cfg.shell and self.cfg.args:
            self.verbose = True
            e = self.cmd(" ".join(self.cfg.args))
            e.wait()
            return
        if not self.cfg.shell:
            return
        super().wait()

## instances

kernel = Kernel()

## functions

def cmd(txt):
    e = kernel.cmd(txt)
    e.wait()
    return e

def init():
    bot = Shell()
    kernel.add(bot)
    thr = launch(bot.start)
    return thr
