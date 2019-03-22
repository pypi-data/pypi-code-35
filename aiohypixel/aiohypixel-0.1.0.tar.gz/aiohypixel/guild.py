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
Custom classes that are related to guild lookups on the Hypixel API
"""

__all__ = ("process_raw_guild", "Guild")

from dataclasses import dataclass
from datetime import datetime
from typing import Union, Dict, Tuple, List

from .shared import APIResponse

LVL_EXP_NEEDED = [
    100000,
    150000,
    250000,
    500000,
    750000,
    1000000,
    1250000,
    1500000,
    2000000,
    2500000,
    2500000,
    2500000,
    2500000,
    2500000,
    3000000,
]


def get_guild_level(exp: int) -> int:
    level = 0
    i = 0
    while True:
        need = LVL_EXP_NEEDED[i]
        exp -= need

        if exp < 0:
            return level

        level += 1

        if i < len(LVL_EXP_NEEDED) - 1:
            i += 1


@dataclass(frozen=True)
class GuildRank:
    name: str
    default: bool
    tag: Union[str, None]
    created_at: datetime
    priority: 1


@dataclass(frozen=True)
class GuildMember:
    uuid: str
    rank: str
    joined_at: datetime
    quest_participation: int


@dataclass(frozen=True)
class Guild:
    """Describes a Hypixel guild"""

    raw_data: APIResponse
    id: str
    name: str
    coins: int
    total_coins: int
    created_at: datetime
    joinable: bool
    tag: Dict[str, str]
    exp: int
    level: int
    preferred_games: List[str]
    ranks: Tuple[GuildRank]
    members: Tuple[GuildMember]
    banner: dict  # The API is kinda messy on this one
    achievements: Dict[str, int]
    exp_by_game: Dict[str, int]


def process_raw_rank(json_data: dict) -> GuildRank:
    created_at = datetime.utcfromtimestamp(json_data["created"] / 1000)
    return GuildRank(
        name=json_data["name"],
        default=json_data["default"],
        tag=json_data["tag"],
        created_at=created_at,
        priority=json_data["priority"],
    )


def process_raw_member(json_data: dict) -> GuildMember:
    joined_at = datetime.utcfromtimestamp(json_data["joined"] / 1000)
    return GuildMember(
        uuid=json_data["uuid"],
        rank=json_data["rank"],
        joined_at=joined_at,
        quest_participation=json_data.get("questParticipation", 0),
    )


def process_raw_guild(json_data: APIResponse) -> Guild:
    """This will process the JSON data and return a Guild object"""
    # Converting UNIX timestamp (ms) to a datetime obj
    created_at = datetime.utcfromtimestamp(json_data["created"] / 1000)

    lvl = get_guild_level(json_data["exp"])

    tag = {
        "text": json_data["tag"],
        "colour": json_data["tagColor"],
        "color": json_data["tagColor"],  # for 'muricans
    }

    ranks = (process_raw_rank(r) for r in json_data["ranks"])

    members = (process_raw_member(m) for m in json_data["members"])

    return Guild(
        raw_data=json_data,
        id=json_data["_id"],
        name=json_data["name"],
        coins=json_data["coins"],
        total_coins=json_data["coinsEver"],
        created_at=created_at,
        tag=tag,
        exp=json_data["exp"],
        level=lvl,
        joinable=json_data.get("joinable", False),
        preferred_games=json_data.get("preferredGames"),
        ranks=tuple(ranks),
        members=tuple(members),
        banner=json_data.get("banner"),
        achievements=json_data["achievements"],
        exp_by_game=json_data["guildExpByGameType"]
    )
