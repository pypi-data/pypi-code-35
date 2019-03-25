# bot/store.py
#
#

""" timestamped JSON file backend. """

import importlib
import json
import logging
import os
import time

import bot
import bot.fleet
import bot.base

from bot.base import cfg, construct, get_cls, get_type, get_types, fn_time
from bot.base import starttime, __version__
from bot.command import args, defaults, types
from bot.utils import days, elapsed, get_exception

## classes

class Store(bot.base.Dotted):

    def all(self, otype, selector=None, index=None, delta=0, showdel=False):
        nr = -1
        for fn in sorted(filenames(otype, delta)):
            nr += 1
            try:
                obj = construct(fn)
            except ModuleNotFoundError:
                continue
            if not showdel and ("_deleted" in obj and obj._deleted):
                continue
            if index is not None and nr != index:
                continue
            yield obj

    def find(self, otype, selector=None, index=None, delta=0, showdel=False):
        nr = -1
        for fn in sorted(filenames(otype, delta)):
            nr += 1
            try:
                obj = construct(fn)
            except AttributeError as ex:
                txt = "ETYPE %s" % fn
                logging.error(txt)
                continue
            except Exception:
                logging.error(get_exception())
                continue
            if not obj:
                continue
            if not showdel and ("_deleted" in obj and obj._deleted):
                continue
            if obj.search(selector):
                if index is not None and nr != index:
                    continue
                yield obj

    def last(self, otype):
        fns = sorted(filenames(otype), key=lambda x: fn_time(x))
        if fns:
            return construct(fns[-1])

## instances

fleet = bot.fleet.Fleet()
store = Store()

## functions

def filenames(ftype, delta=0):
    p = os.path.join(cfg.workdir, ftype)
    now = time.time()
    past = now + delta
    for rootdir, dirs, files in os.walk(p, topdown=True):
        if p not in rootdir:
            continue
        for fn in files:
            fnn = os.path.join(rootdir, fn).split(cfg.workdir)[-1][1:]
            if delta:
                if fn_time(fnn) < past:
                    continue
            yield fnn

def fn_time(daystr):
    daystr = daystr.replace("_", ":")
    datestr = " ".join(daystr.split(os.sep)[-2:])
    datestr = datestr.split(".")[0]
    try:
        t = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
    except ValueError:
        t = 0
    return t

def get_fntype(fn):
    return fn.split(os.sep)[0]

## commands

def find(event):
    res = {x.split(".")[-1].lower() for x in os.listdir(cfg.workdir)}
    if not event.args:
        event.reply("|".join(sorted(types.keys())))
        return
    if not event.index and not event.selector:
        default = args.get(event.args[0], "")
        if default:
            event.selector[default] = ""
            if default not in event.dkeys:
                event.dkeys.append(default)
    if not event.selector:
        func = store.all
    else:
        func = store.find
    stime = time.time()
    res = list(func(event.type, event.selector, event.index, event.delta))
    nr = -1
    for obj in res:
        if not obj:
            event.reply("ETYPE %s" % event.args[0])
            return
        txt = ""
        full = False
        if "d" in event.options:
            event.reply(str(obj))
            continue
        if "f" in event.options:
            full = True
        nr += 1
        if event.dkeys:
            txt = "%s %s" % (event.index or nr, obj.format(event.dkeys, full))
        else:
            txt = "%s %s" % (event.index or nr, obj.format(full=full))
        if "t" in event.options:
            txt += " " + days(obj)
        event.reply(txt)
    logging.warning("ok %s %s" % (len(res), elapsed(time.time()-stime)))

def rm(event):
    res = {x.split(".")[-1].lower() for x in os.listdir(cfg.workdir)}
    if not event.args:
        event.reply("|".join(sorted(res)))
        return
    st = time.time()
    nr = -1
    for obj in store.find(event.type, event.selector, event.index, event.delta):
        nr += 1
        obj._deleted = True
        obj.save()
    event.reply("ok %s %s" % (nr+1, elapsed(time.time()-st)))

def undel(event):
    res = {x.split(".")[-1].lower() for x in os.listdir(cfg.workdir)}
    if not event.args:
        event.reply("|".join(sorted(res)))
        return
    st = time.time()
    nr = -1
    for obj in store.all(event.type, event.selector, event.index, event.delta, showdel=True):
        nr += 1
        obj._deleted = False
        obj.save()
    event.reply("ok %s %s" % (nr+1, elapsed(time.time()-st)))
