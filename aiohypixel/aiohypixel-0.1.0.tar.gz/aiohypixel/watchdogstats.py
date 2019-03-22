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
Stuff for the Watchdog Stats endpoint
"""

__all__ = ("process_raw_wds", "WatchdogStats")

from dataclasses import dataclass

from .shared import APIResponse

def process_raw_wds(json_data: APIResponse):
    return WatchdogStats(
        total=json_data["watchdog_total"],
        rolling_daily=json_data["watchdog_rollingDaily"],
        last_minute=json_data["watchdog_lastMinute"],
        staff_total=json_data["staff_total"],
        staff_rolling_daily=json_data["staff_rollingDaily"]
    )

@dataclass(frozen=True)
class WatchdogStats:
	total: int
	rolling_daily: int
	last_minute: int
	staff_total: int
	staff_rolling_daily: int
