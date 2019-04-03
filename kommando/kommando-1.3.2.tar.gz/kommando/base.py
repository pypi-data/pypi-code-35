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

import os
import sys
import copy
import time
import asyncio
import difflib
import discord
import inspect
import logging
import importlib
import traceback
import collections

from copy import deepcopy
from typing import List, Any, ClassVar
from functools import wraps, lru_cache, partial

class UnfittedKontext(Exception):
    def __init__(self):
        super().__init__('No invocation fit this context')

class KBot(discord.AutoShardedClient):
    """
    The actual bot class
    
    Parameters
    ----------
    **kwargs
        Kwargs passed to AutoShardedClient __init__

    Attributes
    ----------
    Kontext: ClassVar
        A deepcopy of the default Kontext class
    invocations: dict
        The default place to put invocations
    summons: list
        Instances of classes that verifies if the
        bot is being summoned
    """
    def __init__(self, **kwargs):
        discord.AutoShardedClient.__init__(self, **kwargs)
        
        self.Kontext = deepcopy(Kontext)
        self.invocations = {}
        self.summons = []

    def kontext(self, message, cls=None):
        """
        Returns a Kontext instance, based in
        a message

        Parameters
        ----------
        message: discord.Message
            The message that will be used
        cls: ClassVar, optional
            A class that the new kontext will
            be instanced

        Returns
        -------
        Any
            A instance of cls or a instance 
            of Kontext if cls is None
        """
        if not cls:
            return self.Kontext(self, message)
        else:
            return cls(self, message)

    def get_invocation(self, query:str, root:dict=None):
        """
        Searches for a invocation using a
        path-like query in the root

        Parameters
        ----------
        query: str
            The path-like query
        root: dict, optional
            The root to search, if None,
            it will search on self.invocations

        Raises
        ------
        KeyError
            When a part of the path cannot be found
            and the function can't proceed any further
        """
        if root is None:
            root = self.invocations
        for x in query.split('/'):
            root = root[x]
        return root

    def remove_invocation(self, query:str, root:dict=None):
        """
        Removes a invocation, using a
        path-like query in the root

        Parameters
        ----------
        query: str
            The path-like query
        root: dict, optional
            The root to search, if None,
            it will search on self.invocations

        Raises
        ------
        KeyError
            When a part of the path cannot be found
            and the function can't proceed any further
        """
        if root is None:
            root = self.invocations
        self.get_invocation(query, root=root).bot = None
        data = query.rsplit('/', 1)
        if len(data) == 1:
            del root[data[0]]
        else:
            query, key = data
            del self.get_invocation(query, root=root)[key]

    def walk_invocations(self, invocations:dict=None,
                         bfs:bool=True):
        """
        Walks around every invocation
        To search for invocations inside or related to
        a invocation, the invocation needs to have a 
        __nodes__ method

        Parameters
        ----------
        invocations: List[Any], optional
            List of invocations to be searched
            self.invocations if None
        bfs: bool, optional
            If true, the function will use
            breadth-first search (iterative)
            Else, the function will use
            depth-first search (recursive)

        Yields
        ------
        str
            A path to a invocation
        Any
            A invocation object
        """
        if invocations is None:
            invocations = self.invocations
        if bfs:
            deque = collections.deque(invocations.items())
            while True:
                try:
                    k, v = deque.popleft()
                    yield k, v
                    if hasattr(v, '__nodes__'):
                        nodes = v.__nodes__(self, k).items()
                        deque.extend([(k, v) for k, v in nodes
                                    if (k, v) not in deque])
                except IndexError:
                    raise StopIteration
        else:
            for k, v in invocations.items():
                yield k, v
                if hasattr(v, '__nodes__'):
                    nodes = v.__nodes__(self, k)
                    yield from self.walk_invocations(invocations=nodes, 
                                                     bfs=bfs)

    def invocation(self, template:ClassVar, root:str=None, **kwargs):
        """
        Decorator for creating invocations

        Parameters
        ----------
        template: ClassVar
            A class that the new invocation
            will inherit
        root: str, optional
            A path-like query to the root invocation
        **kwargs
            Used as invocation instance attributes

        Return
        ------
        function
            A decorator that returns a invocation
            when used with a Any (f) arg
        """
        def decorator(f):
            frame = inspect.currentframe().f_back
            module = inspect.getmodule(frame)
            module = module.__name__ if module is not None else '__main__'
            section = inspect.getframeinfo(frame).function
            defaults = {'id': f.__name__ if hasattr(f, '__name__') else None, 
                        'module': module, 'section': section, 'root': root,
                        'function': f, 'stats': {}, 'bot': self}
            invocation = template(**{**defaults, **kwargs})
            if root:
                self.get_invocation(root)[invocation.id] = invocation
            else:
                self.invocations[invocation.id] = invocation
            return invocation
        return decorator

    async def parse(self, message:discord.Message,
                    handler=None):
        """
        Takes the message, create a
        kontext and tries to invoke

        If it fails, the exceptions
        can be handled by handler it
        provided

        Parameters
        ----------
        message: discord.Message
            The message that will be parsed
        handler: function, optional
            A function to handle the errors
            
        Return
        ------
        Any
            The return of the invocation call
        
        Raises
        ------
        Exception
            Can raises any exception, especially
            UnfittedKontext
        """
        ktx = self.kontext(message)
        try:
            return await ktx.invoke()
        except Exception as e:
            if handler:
                await asyncio.coroutine(handler)(ktx, e)
            else:
                raise e

class Kontext:
    """
    Implements a context for a message.
    
    Parameters
    ----------
    bot : kommando.Kbot
        A kommando bot instance
    message : discord.Message
        The message that will be used

    Attributes
    ----------
    bot : kommando.Kbot
        A kommando bot instance
    message : discord.Message
        The message that will be used
    path: str or None 
        The path to the invocation
    invocation: Any or None
        A kommando bot invocation
    summon: Any or None
        The instance that verified that
        the bot was summoned
    _message : discord.Message
        A copy of the message, to be used
        by destructive parsing methods
    """
    def __init__(self, bot: KBot, 
                 message:discord.Message):
        self.bot = bot
        self.message = message

        self.path = None
        self.invocation = None
        self.summon = None

        self._message = copy.copy(message)

    @property
    def author(self):
        return self.message.author
    
    @property
    def channel(self):
        return self.message.channel

    @property
    def guild(self):
        return self.message.guild

    @property
    def send(self):
        return self.channel.send

    async def load(self, path:str, invocation:Any):
        """
        Loads the path and the invocation
        This small function exists to be
        easier to make extensions
        
        Parameters
        ----------
        path: str
            The path to the invocation
        invocation: Any
            A kommando bot invocation
        """
        self.path = path
        self.invocation = invocation

    async def fit(self, invocations:List[Any]):    
        """
        Iterates over root invocations to find 
        whose fits the ktx, using __check__

        __check__ needs to return a invocation
        or a false value

        Parameters
        ----------
        invocations: List[Any]
            List of invocations to be searched
        
        Returns
        -------
        str
            The path to the invocation
        Any
            The invocation object

        Raises
        ------
        UnfittedKontext
            When no one fitting invocation has been found
        """
        for k, v in invocations.items():
            inv = await asyncio.coroutine(v.__check__)(self, k)
            if inv:
                return inv[0], inv[1]
        raise UnfittedKontext

    async def invoke(self, *args, **kwargs):
        """
        Tries to invoke something, testing 
        the summons and fitting
        the invocation to bot.invocations

        Parameters
        ----------
        *args
            Args for the invocation call
        **kwargs
            Kwargs for the invocation call

        Raises
        ------
        UnfittedKontext
            When no one fitting invocation have been found

        Return
        ------
        Any
            The return of the invocation call
            or None, if the kontext is ignorable
        """
        if not self.invocation:
            for x in self.bot.summons:
                if await asyncio.coroutine(x)(self):
                    self.summon = x
                    break
            if self.summon is None:
                return None
            path, invocation = await self.fit(self.bot.invocations)
            await self.load(path, invocation)
        return await asyncio.coroutine(self.invocation)(self, *args, **kwargs)
