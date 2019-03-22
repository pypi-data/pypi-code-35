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
Stats dataclasses and other related functions
"""

__all__ = ("BaseGameStats", "BedWarsStats")

from dataclasses import dataclass

BW_XP_PER_PRESTIGE = 489000
BW_LVLS_PER_PRESTIGE = 100

def get_bw_lvl(exp: int) -> int:

    prestige = exp // BW_XP_PER_PRESTIGE
    exp = exp % BW_XP_PER_PRESTIGE

    if prestige > 5:
        over = prestige % 5
        exp += over * BW_XP_PER_PRESTIGE
        prestige -= over

    if exp < 500:
        return 0 + (prestige * BW_LVLS_PER_PRESTIGE)
    if exp < 1500:
        return 1 + (prestige * BW_LVLS_PER_PRESTIGE)
    if exp < 3500:
        return 2 + (prestige * BW_LVLS_PER_PRESTIGE)
    if exp < 5500:
        return 3 + (prestige * BW_LVLS_PER_PRESTIGE)
    if exp < 9000:
        return 4 + (prestige * BW_LVLS_PER_PRESTIGE)

    exp -= 9000

    return (exp / 5000 + 4) + (prestige * BW_LVLS_PER_PRESTIGE)


@dataclass
class BaseGameStats:
    """
    This is the base for every game stats
    """

    raw_data: dict


@dataclass
class BedWarsStats(BaseGameStats):
    """BedWars stats for a player"""

    xp: int
