# bot/store.py
#
#

""" timestamped JSON file backend. """

import bot.base
import importlib
import json
import logging
import os
import time

from bot.base import Dotted, construct, get_cls, get_type, get_types, fn_time, starttime
from bot.command import args, types
from bot.utils import days, elapsed, get_exception

## classes

class Store(Dotted):

    def all(self, otype, selector=None, index=None, delta=0, showdel=False):
        nr = -1
        for fn in sorted(filenames(otype, delta)):
            nr += 1
            try:
                obj = construct(fn)
            except ModuleNotFoundError:
                continue
            if not obj:
                logging.warn("ECONSTRUCT %s" % fn)
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
                logging.error("ETYPE %s" % fn)
                continue
            except Exception:
                logging.error(get_exception())
                continue
            if not showdel and ("_deleted" in dir(obj) and obj._deleted):
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

store = Store()

## functions

def filenames(ftype, delta=0):
    p = os.path.join(bot.base.workdir, ftype)
    now = time.time()
    past = now + delta
    for rootdir, dirs, files in os.walk(p, topdown=True):
        if p not in rootdir:
            continue
        for fn in files:
            fnn = os.path.join(rootdir, fn).split(bot.base.workdir)[-1][1:]
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
    if not event.args:
        event.reply("|".join(sorted(types.keys())))
        return
    if not event.selector and not event.index:
        default = args.get(event.type, "")
        if default:
            event.selector[default] = ""
            if default not in event.dkeys:
                event.dkeys.append(default)
    if not event.args:
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
    if not event.args:
        event.reply("|".join(sorted(get_types())))
        return
    st = time.time()
    nr = -1
    for obj in store.find(event.type, event.selector, event.index, event.delta):
        nr += 1
        obj._deleted = True
        obj.save()
    event.reply("ok %s %s" % (nr+1, elapsed(time.time()-st)))

def undel(event):
    if not event.args:
        event.reply("|".join(sorted(get_types())))
        return
    st = time.time()
    nr = -1
    for obj in store.all(event.type, event.selector, event.index, event.delta, showdel=True):
        nr += 1
        obj._deleted = False
        obj.save()
    event.reply("ok %s %s" % (nr+1, elapsed(time.time()-st)))
