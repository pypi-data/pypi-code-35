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
Custom exceptions related to the Hypixel API and other misc stuff
"""

__all__ = (
    "APIResponse",
    "PlayerNotFound",
    "GuildIDNotValid",
    "HypixelAPIError",
    "InvalidAPIKey",
    "GAME_TYPES_TABLE",
)

import inspect
from typing import NewType, Dict, Union, Mapping, Iterator

GAME_TYPES_TABLE = {
    2: {"type_name": "QUAKECRAFT", "db_name": "Quake", "pretty_name": "Quake"},
    3: {"type_name": "WALLS", "db_name": "Walls", "pretty_name": "Walls"},
    4: {"type_name": "PAINTBALL", "db_name": "Paintball", "pretty_name": "Paintball"},
    5: {
        "type_name": "SURVIVAL_GAMES",
        "db_name": "HungerGames",
        "pretty_name": "Blitz Survival Games",
    },
    6: {"type_name": "TNTGAMES", "db_name": "TNTGames", "pretty_name": "TNT Games"},
    7: {"type_name": "VAMPIREZ", "db_name": "VampireZ", "pretty_name": "VampireZ"},
    13: {"type_name": "WALLS3", "db_name": "Walls3", "pretty_name": "Mega Walls"},
    14: {"type_name": "ARCADE", "db_name": "Arcade", "pretty_name": "Arcade"},
    17: {"type_name": "ARENA", "db_name": "Arena", "pretty_name": "Arena"},
    20: {"type_name": "UHC", "db_name": "UHC", "pretty_name": "UHC Champions"},
    21: {"type_name": "MCGO", "db_name": "MCGO", "pretty_name": "Cops and Crims"},
    23: {
        "type_name": "BATTLEGROUND",
        "db_name": "Battleground",
        "pretty_name": "Warlords",
    },
    24: {
        "type_name": "SUPER_SMASH",
        "db_name": "SuperSmash",
        "pretty_name": "Smash Heroes",
    },
    25: {
        "type_name": "GINGERBREAD",
        "db_name": "GingerBread",
        "pretty_name": "Turbo Kart Racers",
    },
    26: {"type_name": "HOUSING", "db_name": "Housing", "pretty_name": "Housing"},
    51: {"type_name": "SKYWARS", "db_name": "SkyWars", "pretty_name": "SkyWars"},
    52: {
        "type_name": "TRUE_COMBAT",
        "db_name": "TrueCombat",
        "pretty_name": "Crazy Walls",
    },
    54: {"type_name": "SPEED_UHC", "db_name": "SpeedUHC", "pretty_name": "Speed UHC"},
    55: {"type_name": "SKYCLASH", "db_name": "SkyClash", "pretty_name": "SkyClash"},
    56: {"type_name": "LEGACY", "db_name": "Legacy", "pretty_name": "Classic Games"},
    57: {"type_name": "PROTOTYPE", "db_name": "Prototype", "pretty_name": "Prototype"},
    58: {"type_name": "BEDWARS", "db_name": "Bedwars", "pretty_name": "Bed Wars"},
    59: {
        "type_name": "MURDER_MYSTERY",
        "db_name": "MurderMystery",
        "pretty_name": "Murder Mystery",
    },
    60: {
        "type_name": "BUILD_BATTLE",
        "db_name": "BuildBattle",
        "pretty_name": "Build Battle",
    },
    61: {"type_name": "DUELS", "db_name": "Duels", "pretty_name": "Duels"},
}

APIResponse = NewType("APIResponse", Dict[str, Dict[Union[str, int], Union[str, int, bool, dict]]])


class PlayerNotFound(Exception):
    """
    Raised if a player/UUID is not found. This exception can usually be ignored.
    You can catch this exception with ``except aiohypixel.PlayerNotFoundException:`` 
    """

    pass


class GuildIDNotValid(Exception):
    """
    Raised if a Guild is not found using a GuildID. This exception can usually be ignored.
    You can catch this exception with ``except aiohypixel.GuildIDNotValid:`` 
    """

    pass


class HypixelAPIError(Exception):
    """
    Raised if something's gone very wrong and the program can't continue. 
    """

    pass


class UnsuccesfulRequest(Exception):
    """
    Raised when the "success" key from a request is False
    """

    pass


class InvalidAPIKey(Exception):
    """
    Raised if the given API Key is invalid
    """

    pass

def find(func, iterable):
    for i in iterable:
        if func(i):
            return i
    return None

def get(iterable, **attrs):
    def predicate(elem):
        for attr, val in attrs.items():
            nested = attr.split('__')
            obj = elem
            for attribute in nested:
                obj = getattr(obj, attribute)

            if obj != val:
                return False
        return True

    return find(predicate, iterable)


class ImmutableProxy(Mapping):
    """
    An immutable proxy class. Similar to the Proxy class, but works differently.
    
    This is designed to be used for configuration files to convert them to dot-notation
    friendly immutable notation. It is recursive, and will convert list objects to
    tuples, dicts to instances of this class, and protects from recursive lookup issues.

    Source:
        https://gitlab.com/koyagami/libneko/blob/master/libneko/aggregates.py#L333-396

    Author:
        Espy/Ko Yagami (https://gitlab.com/koyagami)
    """

    def __init__(self, kwargs, *, recurse=True):
        """
        If recurse is True, it converts all inner dicts to this type too.
        """
        if not isinstance(kwargs, dict):
            raise TypeError(f"Expected dictionary, got {type(kwargs).__name__}")

        if recurse:
            self.__dict = self._recurse_replace(kwargs)
        else:
            self.__dict = kwargs

    def __getattr__(self, item):
        try:
            return self.__dict[item]
        except KeyError:
            raise AttributeError(item) from None

    def __getitem__(self, item):
        return self.__dict[item]

    def __len__(self) -> int:
        return len(self.__dict)

    def __iter__(self) -> Iterator:
        return iter(self.__dict)

    def __str__(self):
        return str(self.__dict)

    def __repr__(self):
        return repr(self.__dict)

    def __hash__(self):
        return object.__hash__(self)

    @classmethod
    def _recurse_replace(cls, obj, already_passed=None):
        if already_passed is None:
            already_passed = []

        new_dict = {}
        for k, v in obj.items():
            if isinstance(v, dict):
                if v in already_passed:
                    new_dict[k] = v
                else:
                    already_passed.append(v)
                    new_dict[k] = cls._recurse_replace(v, already_passed)
            elif isinstance(v, list):
                new_dict[k] = tuple(v)
            else:
                new_dict[k] = v

        return cls(new_dict, recurse=False)

