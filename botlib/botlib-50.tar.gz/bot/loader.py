# bot/loader.py
#
#

""" module loader. """

import importlib
import logging
import pkgutil
import types

import bot
import bot.store
import bot.tasks
import bot.utils

from bot.base import Dotted, cfg
from bot.tasks import launch
from bot.utils import get_exception, get_name

## defines

aliases = {
           "a": "announce",
           "c": "show cmds",
           "cfg": "show cfg",
           "f": "find",
           "h": "show help",
           "l": "show types",
           "m": "show mods",
           "ps": "show tasks",
           "s": "show",
           "v": "show version",
}

names = {
    "ed": "bot.edit",
    "fetch": "bot.rss",
    "find": "bot.store",
    "load": "bot.loader",
    "log": "bot.entry",
    "meet": "bot.users",
    "rm": "bot.store",
    "rss": "bot.rss",
    "show": "bot.cmds",
    "stop": "bot.tasks",
    "todo": "bot.entry",
    "undel": "bot.store",
    "unload": "bot.loader"
}

## classes

class Loader(Dotted):

    def __init__(self):
        super().__init__()
        self.aliases = aliases
        self.names = names
        self.handlers = Dotted()
        self.table = Dotted()

    def direct(self, name, package=None):
        txt = "direct %s" % name
        logging.debug(txt)
        return importlib.import_module(name, package)

    def get_aliased(self, txt):
        spl = txt.split()
        if spl and spl[0] in self.aliases:
            cmd = spl[0]
            v = self.aliases.get(cmd, None)
            if v:
                spl[0] = cmd.replace(cmd, v)
        txt = " ".join(spl)
        return txt

    def get_handler(self, cmd):
        val = self.handlers.get(cmd, None)
        if not val:
            modname = self.names.get(cmd, None)
            if modname:
                self.load_mod(modname)
            val = self.handlers.get(cmd, None)
        return val

    def init(self, m):
        func = getattr(m, "init", None)
        if func:
            thr = launch(func)
            logging.warning("init %s" % get_name(m))
            return thr

    def load_mod(self, name, mod=None):
        global names
        mod = mod or self.direct(name)
        self.table[name] = mod
        for key, func, modname in self.scan(mod):
            self.handlers[key] = func
            names[key] = modname
        return mod

    def register(self, cmd, handler):
        self.handlers[cmd] = handler

    def scan(self, mod):
        for key in dir(mod):
            if key.startswith("_"):
                continue
            func = getattr(mod, key, None)
            if func and isinstance(func, types.FunctionType):
                if "event" in func.__code__.co_varnames:
                    yield (key, func, mod.__name__)

    def unload(self, modname):
        mod = self.table[modname]
        for key, func, name in self.scan(mod):
            if name == modname:
                try:
                    del self.handlers[key]
                    del self.names[key]
                except KeyError:
                    pass

    def walk(self, modname):
        mods = []
        mod = self.load_mod(modname)
        if "__path__" in dir(mod):
            for nn in pkgutil.walk_packages(mod.__path__, modname+'.'):
                mods.append(self.load_mod(nn[1]))
        else:
            mods.append(mod)
        return mods

## commands

def load(event):
    if not event.args:
        loader = Loader()
        loader.walk("bot")
        event.reply("|".join(sorted([x.split(".")[-1] for x in loader.table.keys()])))
        return
    from bot.kernel import kernel
    name = event.args[0]
    mod = kernel.walk(name)
    event.reply("%s loaded" % name)

def unload(event):
    if not event.args:
        loader = Loader()
        loader.walk("bot")
        event.reply("|".join(loader.table.keys()))
        return
    from bot.kernel import kernel
    name = event.args[0]
    try:
        kernel.unload(name)
    except KeyError:
        event.reply("%s is not loaded." % name)        
        return
    event.reply("unload %s" % name)
