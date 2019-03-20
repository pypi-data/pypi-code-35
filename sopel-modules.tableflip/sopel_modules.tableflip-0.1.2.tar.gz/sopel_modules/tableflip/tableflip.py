# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division
import random

from sopel.module import commands, example, rule
from sopel import formatting
from sopel import logger


LOG = logger.get_logger(__name__)

HI_LIST = [
    "( ･ω･)ﾉ",
    "( ^_^)／",
    "(^o^)/",
    "( ´ ▽ ` )ﾉ",
    "(=ﾟωﾟ)ﾉ",
    "( ・_・)ノ",
    "(。･∀･)ﾉ",
    "(*ﾟ͠ ∀ ͠)ﾉ",
    "(♦亝д 亝)ﾉ",
    "( *՞ਊ՞*)ﾉ",
    "(｡Ő▽Ő｡)ﾉﾞ",
    "(ஐ╹◡╹)ノ",
    "(✧∇✧)╯",
    "(^▽^)/ ʸᵉᔆᵎ",
    "(。･д･)ﾉﾞ",
    "(◍˃̶ᗜ˂̶◍)ﾉ”",
    "(*´･д･)ﾉ",
    "|。･ω･|ﾉ",
    "(ه’́⌣’̀ه )／",
    "ヽ(´･ω･`)､",
    "ヘ(°￢°)ノ",
    "＼(-_- )",
    "(¬_¬)ﾉ",
    "(;-_-)ノ",
    "(^-^*)/",
    "＼( ･_･)",
    "ヾ(-_-;)",
    "|ʘ‿ʘ)╯"
]

# Map the .tf <command> to a function
COMMAND_MAPPING = {
    "hi": "_hello",
    "hello": "_hello",

    "battle": "_battle",
    "b": "_battle",

    "covfefe": "_covfefe",
    "c": "_covfefe",

    "dude": "_dude",
    "d": "_dude",

    "fat": "_fat",
    "f": "_fat",

    "finger": "_finger",
    "g": "_finger",

    "hercules": "_hercules",
    "h": "_hercules",

    "jedi": "_jedi",
    "j": "_jedi",

    "magic": "_magic",
    "m": "_magic",

    "rage": "_rage",
    "r": "_rage",

    "bear": "_bear",
    "z": "_bear",
}


# matching exactly @!
@rule(r'\@\?$')
def flip_help(bot, trigger):
    # flip = "(╯°□°)╯︵ ┻━┻ ".decode("utf-8")
    flip = formatting.color("(╯°□°)╯︵ ┻━┻ ", formatting.colors.RED)
    bot.say("Welcome to Table flipping bot.")
    bot.say(flip)
    bot.say("@!           - Hello.")
    bot.say("@!b <nick>   - Battle another nick table flip.")
    bot.say("@!c          - Covfefe table flip.")
    bot.say("@!d <nick>   - Battle win another nick table flip.")
    bot.say("@!f          - Fat table flip.")
    bot.say("@!g          - The Finger table flip.")
    bot.say("@!h          - Hercules table flip.")
    bot.say("@!j          - Jedi table flip.")
    bot.say("@!m          - Magic table flip.")
    bot.say("@!r          - Rage table flip.")
    bot.say("@!t          - Standard table flip.")
    bot.say("@!z          - Bear table flip.")


def _prep_colors(nick, flip):
    return (formatting.color(nick, formatting.colors.BLUE),
            formatting.color(flip, formatting.colors.RED))


def _build_msg(trigger, flip, replace_str=None):
    nick, flip = _prep_colors(trigger.nick, flip)
    msg = "%s %s" % (nick, flip)
    if replace_str and trigger:
        other = str(trigger).replace(replace_str, '')
        return msg + other
    else:
        return msg


@commands("tf", "tableflip")
@example(".tf hi #pewp")
@example(".tf h #pewp")
@example(".tf c #pewp")
def tf(bot, trigger):
    """Send a table flip to a channel."""
    args = trigger.args[1].split(' ')
    # LOG.warning("Command args %s" % args)

    try:
        tf_function = args[1]
        tf_channel = args[2]
        func = COMMAND_MAPPING[tf_function]
    except Exception as e:
        bot.say("I don't know what you want me to do", trigger.nick)
        LOG.error(e)
    else:
        msg = globals()[func](bot, trigger)
        bot.say(msg, tf_channel)


def _hello(bot, trigger):
    index = random.randint(0, len(HI_LIST) - 1)
    # flip = hi_list[index].decode("utf-8")
    flip = HI_LIST[index]
    msg = _build_msg(trigger, flip)
    return msg


# matching exactly @!
@rule(r'\@\!$')
def hello(bot, trigger):
    bot.say(_hello(bot, trigger))


# matching @!b
# also appends anything after @!b to end of message
@rule(r'\@\!b')
def flip_battle(bot, trigger):
    flip = "(╯°□°)╯︵ ┻━┻ ︵ ╯(°□° ╯)"
    msg = _build_msg(trigger, flip, replace_str="@!b")
    bot.say(msg)


def _covfefe(bot, trigger):
    flip = "༼ノಠل͟ಠ༽ノ ︵ ┻━┻"
    return _build_msg(trigger, flip)


# matching @!c
@rule(r'\@\!c')
def flip_covfefe(bot, trigger):
    bot.say(_covfefe(bot, trigger))


# matching @!d
# also appends anything after @!d to end of message
@rule(r'\@\!d')
def flip_dude(bot, trigger):
    flip = "(╯°Д°）╯︵ /(.□ . )"
    msg = _build_msg(trigger, flip, replace_str='@!d')
    bot.say(msg)


def _fat(bot, trigger):
    flip = "(ノ ゜Д゜)ノ ︵ ┻━┻"
    return _build_msg(trigger, flip)


# matching @!f
@rule(r'\@\!f')
def flip_fat(bot, trigger):
    bot.say(_fat(bot, trigger))


def _finger(bot, trigger):
    flip = "╭∩╮◕ل͜◕)╭∩╮  ︵┻┻"
    return _build_msg(trigger, flip)


# matching @!g
@rule(r'\@\!g')
def flip_finger(bot, trigger):
    bot.say(_finger(bot, trigger))


def _hercules(bot, trigger):
    flip = "(/ .□.) ︵╰(゜Д゜)╯︵ /(.□. )"
    return _build_msg(trigger, flip)


# matching @!h
@rule(r'\@\!h')
def flip_hercules(bot, trigger):
    bot.say(_hercules(bot, trigger))


def _jedi(bot, trigger):
    flip = "(._.) ~ ︵ ┻━┻"
    return _build_msg(trigger, flip)


# matching @!j
@rule(r'\@\!j')
def flip_jedi(bot, trigger):
    bot.say(_jedi(bot, trigger))


def _magic(bot, trigger):
    flip = "༼∩ຈل͜ຈ༽つ━☆ﾟ.*･｡ﾟ ︵ ┻━┻"
    return _build_msg(trigger, flip)


# matching @!m
@rule(r'\@\!m')
def flip_magic(bot, trigger):
    bot.say(_magic(bot, trigger))


def _rage(bot, trigger):
    flip = "(ノಠ益ಠ)ノ彡┻━┻"
    return _build_msg(trigger, flip)


# matching @!r
@rule(r'\@\!r')
def flip_rage(bot, trigger):
    bot.say(_rage(bot, trigger))


def _table(bot, trigger):
    flip = "(╯°□°)╯︵ ┻━┻ "
    return _build_msg(trigger, flip)


# matching @!t
@rule(r'\@\!t')
def flip_table(bot, trigger):
    bot.say(_table(bot, trigger))


def _bear(bot, trigger):
    flip = "ʕノ•ᴥ•ʔノ ︵ ┻━┻"
    return _build_msg(trigger, flip)


# matching @!z
@rule(r'\@\!z')
def flip_bear(bot, trigger):
    bot.say(_bear(bot, trigger))
