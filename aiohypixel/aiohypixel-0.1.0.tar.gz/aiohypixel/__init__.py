#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

# MIT License

# Copyright (c) 2018-2019 Tmpod

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This is an asynchronous Hypixel API wrapper written in Python
Compatible with Python3.6 and up

NOTE: It's highly recommended that you setup logging for this module! A lot of
info that you may not want to miss is reported through there. Doing it for
aiohttp might also be good (INFO level is generaly enough)
"""

from . import (
    shared,
    session,
    player,
    guild,
    keys,
    boosters,
    friends,
    watchdogstats,
    stats
    )

from .session import *
from .shared import *
from .player import *
from .stats import *
from .guild import *
from .boosters import *
from .keys import *
from .friends import *
from .watchdogstats import *


__author__ = "Tmpod"
__url__ = f"https://gitlab.com/{__author__}/aiohypixel/"
__version__ = "0.0.1a"
__licence__ = "MIT"
__copyright__ = f"Copyright (c) 2018-2019 {__author__}"
