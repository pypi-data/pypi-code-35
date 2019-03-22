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
Stuff for the keys endpoint
"""

__all__ = ("process_raw_key", "Key")

from dataclasses import dataclass
from datetime import datetime

from .shared import APIResponse

def process_raw_key(json_data: APIResponse):
    return Key(
        owner_uuid=json_data["ownerUuid"],
        value=json_data["key"],
        total_queries=json_data["totalQueries"],
        queries_in_past_min=json_data.get("queriesInPastMin"),
    )

@dataclass(frozen=True)
class Key:
    owner_uuid: str
    value: str  # The actual key
    total_queries: int
    queries_in_past_min: int
