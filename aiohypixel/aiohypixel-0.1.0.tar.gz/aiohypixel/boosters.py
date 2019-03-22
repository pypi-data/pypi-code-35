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
Stuff for the boosters endpoint
"""

__all__ = ("process_raw_booster", "Booster")

from dataclasses import dataclass
from datetime import datetime
from typing import Union, Tuple

from .shared import APIResponse, GAME_TYPES_TABLE

def process_raw_booster(json_data: APIResponse):
    activated_at = datetime.utcfromtimestamp(json_data["dateActivated"] / 1000)
    return Booster(
        purchaser_uuid=json_data["purchaserUuid"],
        amount=json_data["amount"],
        original_length=json_data["originalLength"],
        current_length=json_data["length"],
        game_type=json_data["gameType"],
        game=GAME_TYPES_TABLE.get(json_data["gameType"]),
        activated_at=activated_at,
        stacked=json_data.get("stacked"),
    )

@dataclass(frozen=True)
class Booster:
    purchaser_uuid: str
    amount: int
    original_length: int
    current_length: int
    game_type: int
    game: str
    activated_at: datetime
    stacked: Union[
        bool, Tuple[str], None
    ]  # not sure what this is... I'll get back here soon
