# bot/cmds.py
#
#

""" basic command set. """

import os
import time

import bot
import bot.base
import bot.fleet
import bot.loader
import bot.store
import bot.tasks
import bot.utils

from bot.base import cfg, get_types, starttime, __version__
from bot.kernel import kernel
from bot.tasks import running
from bot.utils import elapsed

## instances

fleet = bot.fleet.Fleet()
store = bot.store.Store()

## commands

def show(event):
    bot = kernel.get_bot(event.orig)
    try:
        cmd, *args = event.args
    except ValueError:
        event.reply("alias|cfg|cmds|fleet|keys|mods|uptime|version")
        return
    if cmd == "alias":
        event.reply(",".join(['%s=%s' % x for x in kernel.aliases.items()]))
    elif cmd == "cfg":
        if len(args):
            type = "bot.%s.Cfg" % args[0]
            event.reply(store.last(type))
        else:
            event.reply(cfg)
    elif cmd == "cmds":
        if args:
            event.reply(",".join(sorted([x for x in kernel.names.keys() if args[0] in str(x)])))
        else:
            event.reply(",".join(sorted(kernel.names.keys())))
    elif cmd == "fleet":
        try:
            nr = int(args[0])
        except (IndexError, ValueError):
            event.reply(str([bot.base.get_type(b) for b in kernel.bots]))
            return
        try:
            event.reply(str(kernel.bots[nr]))
        except IndexError:
            pass
    elif cmd == "keys":
        if not args:
            res = {x.split(".")[-1].lower() for x in os.listdir(cfg.workdir)}
            event.reply("|".join(sorted(res)))
            return
        for otype in get_types(args[0]):
            l = store.last(otype)
            if l:
                res = [x for x in l.keys() if not x.startswith("_")]
                event.reply("|".join(res))
    elif cmd == "mods":
        l = bot.loader.Loader()
        l.walk("bot")
        res = {x.split(".")[-1].lower() for x in l.table.keys()}
        event.reply("|".join(sorted(res)))
    elif cmd == "help":
        res = ""
        for key, val in kernel.aliases.items():
            res += "%s (%s) " % (key, val.split()[-1])
        if res:
            event.reply(res)
    elif cmd == "tasks":
        psformat = "%-8s %-60s"
        result = []
        try:
            getnr = int(event.args[0])
        except (ValueError, IndexError):
            getnr = None
        for thr in sorted(running(), key=lambda x: x.getName()):
            obj = bot.base.Dotted()
            obj.update(vars(thr))
            if getattr(obj, "sleep", None):
                up = obj.sleep - int(time.time() - obj.state.latest)
            else:
                up = int(time.time() - starttime)
            thrname = thr.getName()
            result.append((up, thrname, obj))
        nr = -1
        for up, thrname, obj in sorted(result, key=lambda x: x[0]):
            nr += 1
            if getnr is not None and getnr == nr:
                event.reply(obj)
                return
            res = "%s %s" % (nr, psformat % (elapsed(up), thrname[:30]))
            event.reply(res)
    elif cmd == "types":
        event.reply("|".join(sorted({x.split(".")[-1].lower() for x in os.listdir(cfg.workdir)})))
    elif cmd == "version":
        event.reply("%s %s" % (cfg.name.upper(), cfg.version))
    elif cmd == "uptime":
        event.reply(elapsed(time.time() - starttime))
