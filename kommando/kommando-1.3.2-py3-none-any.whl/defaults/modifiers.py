"""
MIT License

Copyright (c) 2019 Andre Augusto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time
import asyncio

from functools import wraps
from collections import deque
from kommando.defaults.types import Role
from kommando.defaults.errors import ModifierError

def _get_unique(name, l):
    n = 0
    result = name
    while True:
        if result not in l:
            return result
        result = f'{name}_{n}'
        n += 1

def _call_checker(f):
    def decorator(f2):
        @wraps(f2)
        async def __call__(self, ktx, *args, **kwargs):
            modify = kwargs['modify'] \
                        if 'modify' in kwargs \
                        else True
            if not modify or await asyncio.coroutine(f)(ktx):
                return await asyncio.coroutine(f2)(ktx, *args, **kwargs)
        return __call__
    return decorator

def _set_call(inv, f):
    inv.__class__ = type(type(inv).__name__, (inv.__class__,), 
                         {**inv.__dict__, '__call__': f})

def checker(f):
    def modifier(inv):
        _set_call(inv, _call_checker(f)(inv.__call__))
        return inv
    return modifier

def concurrency(level=3):
    if level > 3:
        raise ValueError(f"Level {level} don't exist")
    def modifier(inv):
        if 'instances' not in inv.stats:
            instances = inv.stats['instances'] = []
        def decorator(f):
            @wraps(f)
            async def __call__(self, ktx, *args, **kwargs):
                if ktx.guild is None:
                    ids = [0, ktx.channel.id, ktx.channel.id, ktx.author.id]
                else:
                    ids = [0, ktx.guild.id, ktx.channel.id, ktx.author.id]
                req_id = ids[level]
                
                modify = kwargs['modify'] \
                         if 'modify' in kwargs \
                         else True

                if not modify or req_id not in instances:
                    instances.append(req_id)
                    try:
                        c = asyncio.coroutine(f)
                        return await c(ktx, *args, **kwargs)
                    except Exception as err:
                        raise err
                    finally:
                        del instances[instances.index(req_id)]
                raise ModifierError(0, level=level)
            return __call__
        _set_call(inv, decorator(inv.__call__))
        return inv
    return modifier

def cooldown(name='cooldown', uses=1, trigger=5, wait=5, level=3, count_fail=False):
    if level > 3:
        raise ValueError(f"Level {level} don't exist")
    def modifier(inv):
        cname = _get_unique(name, inv.stats)
        d = inv.stats[cname] = {}
        async def check(ktx, d=d):
            if ktx.guild is None:
                ids = [0, ktx.channel.id, ktx.channel.id, ktx.author.id]
            else:
                ids = [0, ktx.guild.id, ktx.channel.id, ktx.author.id]
            req_id = ids[level]

            if req_id not in d:
                d[req_id] = [False, deque([]), -1]

            if not d[req_id][0] or count_fail:
                d[req_id][1].append(time.time())
                if len(d[req_id][1]) > uses:
                    d[req_id][1].popleft()
                
            if not d[req_id][0]:
                diff = d[req_id][1][-1] - d[req_id][1][0]
                if len(d[req_id][1]) == uses and diff <= trigger:
                    d[req_id][0] = True
            else:
                diff = time.time() - d[req_id][1][-1]
                if diff > wait:
                    del d[req_id]
                else:
                    d[req_id][2] += 1
                    status = wait - diff
                    retries = d[req_id][2]
                    raise ModifierError(1, name=cname, uses=uses, 
                                        trigger=trigger, wait=wait, 
                                        level=level, status=status,
                                        retries=retries)
            return True
                
        return checker(check)(inv)
    return modifier

def need_perms(*perms, mode='all', target=None):
    if mode not in ['all', 'any']:
        raise ValueError('Unknown mode')
    async def check(ktx):
        p = []
        r = ktx.author.roles if target is None else target.roles
        for role in r:
            p.extend(role.permissions)
        p = set([x[0] for x in p if x[1]])
        if eval(mode)([x in p for x in perms]):
            return True
        else:
            raise ModifierError(2, perms=perms, 
                                mode=mode, target=target)
    return checker(check)

def need_roles(*roles, mode='all', target=None):
    async def check(ktx):
        r = ktx.author.roles if target is None else target.roles
        if eval(mode)([Role(ktx, x) in r for x in roles]):
            return True
        raise ModifierError(3, roles=roles, 
                            mode=mode, target=target)
    return checker(check)

def _evaluator(source, num):
    async def check(ktx):
        if eval(source):
            return True
        else:
            raise ModifierError(num)
    return checker(check)

owner_only = _evaluator("ktx.author.id in ktx.bot.owners", 4)
dm_only = _evaluator("ktx.guild is None", 5)
guild_only = _evaluator("ktx.guild is not None", 6)
nsfw_only = _evaluator('ktx.message.channel.is_nsfw()', 7)
safe_only = _evaluator('not ktx.message.channel.is_nsfw()', 8)
