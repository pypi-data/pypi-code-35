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
This is just a little *crude* interface for the wrapper.
"""

from .session import HypixelSession
import logging, asyncio, sys
from shutil import get_terminal_size

WIN_SIZE = get_terminal_size()

def fmtp(s: str) -> str:
    """Just prints the string with a little delimiter around it"""
    ndash = ("-" * (len(s) - 2)) if len(s) <= WIN_SIZE.columns else "-" * (WIN_SIZE.columns - 2)
    print(f"\n<{ndash}>\n{s}\n<{ndash}>\n")

try:
    api_key = sys.argv[1]
except IndexError:
    fmtp("You must provide an API key!")
else:
    try:
        get_type = sys.argv[2]
    except IndexError:
        fmtp("You must provide a get method!")
    else:      
        logging.basicConfig(level="DEBUG")

        try:
            query = sys.argv[3]
        except IndexError:
            query = None

        loop = asyncio.get_event_loop()


        async def main(get_type: str, query: str = None) -> None:
            session = await HypixelSession(api_key)

            try:
                if query is None:
                    fmtp(str(await (getattr(session, f"get_{get_type}"))()))
                    return
                
                fmtp(str(await (getattr(session, f"get_{get_type}"))(query)))

            except AttributeError:
                fmtp("Invalid!")

        loop.run_until_complete(main(get_type, query))
