
# bot/fleet.py
#
#

""" list of bots. """

import bot.base

## classes

class Fleet(bot.base.Dotted):

    bots = []

    def __iter__(self):
        return iter(self.bots)

    def add(self, bot):
        Fleet.bots.append(bot)
        return self

    def announce(self, txt):
        for bot in Fleet.bots:
            if bot is self:
                continue
            bot.announce(str(txt))

    def by_type(self, btype):
        res = None
        for bot in Fleet.bots:
            if str(btype).lower() in str(type(bot)).lower():
                res = bot
        return res

    def get_bot(self, bid):
        res = None
        for bot in Fleet.bots:
            if str(bid) in repr(bot):
                res = bot
                break
        return res

    def get_firstbot(self):
        return self.bots[0]

    def match(self, m):
        res = None
        for bot in Fleet.bots:
            if m.lower() in repr(bot):
                res = bot
                break
        return res

    def remove(self, bot):
        Fleet.bots.remove(bot)

    def say(self, botid, channel, txt):
        bot = self.get_bot(botid)
        if bot:
            bot.say(botid, channel, txt)

    def stop(self):
        for bot in Fleet.bots:
            if bot is self:
                continue
            bot.stop()

    def wait(self):
        for bot in Fleet.bots:
            bot.wait()
