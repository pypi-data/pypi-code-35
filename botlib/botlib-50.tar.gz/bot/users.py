# bot/users.py
#
#

""" manage users. """

import logging

import bot
import bot.base
import bot.fleet
import bot.store

## exceptions

class EUSER(Exception):
    pass

## classes

class User(bot.base.Dotted):

    def __init__(self):
        super().__init__()
        self.user = ""
        self.perms = []

class Users(bot.store.Store):

    userhosts = bot.base.Dotted()

    def allowed(self, origin, perm):
        perm = perm.upper()
        user = self.get_user(origin)
        if user:
            if perm in user.perms:
                logging.warn("allow %s %s" % (origin, perm))
                return True
        logging.error("denied %s %s" % (origin, perm))
        return False

    def delete(self, origin, perm):
        for user in self.get_users(origin):
            try:
                user.perms.remove(perm)
                user.save()
                return True
            except ValueError:
                pass

    def get_users(self, origin=""):
        return self.all("bot.users.User")

    def get_user(self, origin):
        if origin in cache:
            return cache[origin]
        s = {"user": origin}
        res = list(self.find("bot.users.User", s))
        if res:
            u = res[-1]
            cache[origin] = u
            return u

    def meet(self, origin, perms=[]):
        logging.warning("meet %s" % origin)
        user = self.get_user(origin)
        if not user:
            user = User()
        user.user = origin
        user.perms = perms + ["USER", ]
        if perms:
            user.perms.extend(perms.upper())
        user.save(timed=True)
        return user

    def oper(self, origin):
        logging.warn("oper %s" % origin)
        user = self.get_user(origin)
        if not user:
            user = User()
            user.user = origin
            user.perms = ["OPER", "USER"]
            user.save()
        return user

    def perm(self, origin, permission):
        user = self.get_user(origin)
        if not user:
            raise EUSER(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            user.save()
        return user

## instances

cache = bot.base.Dotted()
fleet = bot.fleet.Fleet()
users = Users()

## commands

def meet(event):
    try:
        origin, *perms = event.args[:]
    except ValueError:
        event.reply("|".join(sorted(users.userhosts.keys())))
        return
    origin = users.userhosts.get(origin, origin)
    u = users.meet(origin, perms)
    event.reply("added %s" % u.user)

