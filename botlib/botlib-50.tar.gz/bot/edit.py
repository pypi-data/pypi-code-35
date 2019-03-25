# bot/edit.py
#
#

""" JSON file editor. """

import json
import os

import bot
import bot.base
import bot.store

from bot.base import cfg, get_cls, get_types, fn_time
from bot.utils import hd

## instances

store = bot.store.Store()

## commands

def ed(event):
    if not cfg.workdir:
        cfg.workdir = hd(".bot")
        cdir(cfg.workdir)
    if not event.args:
        event.reply("|".join(os.listdir(cfg.workdir)))
        return
    types = get_types(event.type)
    if not types:
        event.reply("ETYPE %s" % event.type)
        return
    if len(types) > 1:
        event.reply("|".join(types))
        return
    obj = store.last(types[0])
    if not obj:
        try:
            obj = get_cls(event.type)()
        except ModuleNotFoundError:
            event.reply("not found %s" % event.type)
            return
    if not event.setter:
        event.reply(obj)
        return
    for key, value in event.setter.items():
        val = None
        v = None
        try:
            if "," in value:
                value = value.split(",")
            if type(value) == list:
                v = "%s" % str(value)
                v = v.replace("'",'"')
            else:
                v = '"%s"' % value
            val = json.loads(v)
        except json.decoder.JSONDecodeError:
            event.reply("%s is not JSON" % value)
            continue
        try:
            val = int(val)
        except (TypeError, ValueError):
            try:
                val = float(val)
            except (TypeError, ValueError):
                pass
        t = type(val)
        if val in ["True", "true"]:
            obj.set_attr(key, True)
        elif val in ["False", "false"]:
            obj.set_attr(key, False)
        elif t == list:
            obj.set_attr(key, val)
        elif t == str:
            obj.set_attr(key, val)
        else:
            obj[key] = val
    fn = obj.save()
    event.reply("ok %s" % fn)
    #event.reply(obj)
