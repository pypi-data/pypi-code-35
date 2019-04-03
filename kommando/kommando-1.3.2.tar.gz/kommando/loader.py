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
import asyncio
import inspect
import logging
import kommando
import importlib
import traceback

from itertools import tee
from typing import Any, Callable
from collections import namedtuple

class Loader:
    '''
    Implements a default way of loading and reloading extensions.
    
    Parameters
    ----------
    bot : kommando.Kbot
        A kommando bot instance

    Attributes
    ----------
    dict : dict
        A dict to hold data from
        loaded extensions
    log : logging.Logger
        A logger for dumping loading
        info/errors
    '''
    def __init__(self, bot:kommando.KBot):
        self.bot = bot
        self.dict = {}
        self.log = logging.getLogger('kommando.loader')
    
    def add(self, module:str):
        '''
        Imports and add a module to the loaded modules
        without loading it sections.

        Parameters
        ----------
        module : str
            The importable name of the module.
        '''
        ref = importlib.import_module(module)
        self.dict[ref.__name__] = {'ref': ref, 'sections': {}}

    def remove(self, module:str):
        '''
        Switches every section to the final state
        and delete the module.

        Parameters
        ----------
        module : str
            The importable name of the module.

        '''
        for x in self.dict[module]['sections']:
            self.switch_until_finished(module, x)
        del self.dict[module]

    def reload(self, module:str):
        '''
        Basically the same as remove(module) and then
        add(module), but uses importlib.reload instead of
        importlib.import_module.

        Parameters
        ----------
        module : str
            The importable name of the module.
        '''
        ref = self.dict[module]['ref']
        backup = ref.__dict__.copy()
        self.remove(module)
        try:
            ref = importlib.reload(ref)
        except Exception as err:
            ref.__dict__.update(backup)
            raise err
        finally:
            self.dict[ref.__name__] = {'ref': ref, 'sections': {}}

    def load_section(self, module:str, section:str, switch:int=1):
        '''
        Loads a section from a extension.

        Parameters
        ----------
        module : str
            The importable name of the module.
        section : str
            The name of the generator function.
        switch: int, optional
            Times the section state should be switched.
        '''
        data = self.dict[module]
        ref = data['ref']
        if hasattr(ref, section):
            x = getattr(ref, section)
            if inspect.isgeneratorfunction(x) and \
                not x.__name__.startswith('_') and \
                x.__module__ == ref.__name__:
                
                s = data['sections'][x.__name__] = {}
                s['function'] = x
                s['generator'] = x(self.bot)
                s['state'] = None
                self.log.info(f'Section {section} from {module} load')
                self.switch(module, section, times=switch)
                return True
        return False

    def load_sections(self, module:str, switch:int=1, exclude=None):
        '''
        Loads all sections from a extension.

        Parameters
        ----------
        module : str
            The importable name of the module.
        switch: int, optional
            Times the section state should be switched
            (per section).
        '''
        exclude = None or []
        for x in dir(self.dict[module]['ref']):
            if x not in exclude:
                self.load_section(module, x, switch=switch)

    def switch(self, module:str, section:str, 
               times:int=1, reset:bool=True) -> Any:
        '''
        Switches the section state.

        Parameters
        ----------
        module : str
            The importable name of the module.
        section : str
            The name of the generator function.
        times: int, optional
            Times the section state should be switched.
        reset: bool, optional
            If True, another generator is created after
            the actual was exhausted.

        Returns
        -------
        Any
            The actual state of the generator,
            it expects a string, but as this is defined
            by user, anything can be returned.
        '''
        if times > 0:
            for _ in range(times):
                s = self.dict[module]['sections'][section]
                try:
                    s['state'] = next(s['generator'])
                except StopIteration:
                    if reset:
                        s['generator'] = s['function'](self.bot)
                        s['state'] = next(s['generator'])
                    else:
                        raise StopIteration
            self.log.info(f'{module}/{section} state changed to {s["state"]}')
            return s["state"]

    def switch_until_state(self, module:str, section:str, state:Any, 
                           tries=10, skip=0) -> bool:
        '''
        Switches the section state until
        it reaches some user-defined value.

        Parameters
        ----------
        module : str
            The importable name of the module.
        section : str
            The name of the generator function.
        state: Any
            The state that the section should reach.
        tries: int, optional
            The number of times the function 
            will try to change the section state.
        skip: int, optional
            How many states should be skipped first
            This can be used to make the section
            reach the same state again.

        Returns
        -------
        bool
            True if the section reached the wanted state, 
            False otherwise.
        '''
        s = self.dict[module]['sections'][section]
        i = 0
        for _ in range(skip):
            self.switch(module, section)
            tries -= 1
        while s['state'] != state:
            self.switch(module, section)
            if i >= tries:
                break
            i += 1
        return s['state'] == state

    def switch_until_finished(self, module:str, section:str):
        '''
        Switches the section state until
        its generator is exhausted.

        Parameters
        ----------
        module : str
            The importable name of the module.
        section : str
            The name of the generator function.
        '''
        while True:
            try:
                self.switch(module, section, reset=False)
            except StopIteration:
                break

    def get_state(self, module:str, section:str):
        '''
        Get the section state and returns.

        Parameters
        ----------
        module : str
            The importable name of the module.
        section : str
            The name of the generator function.

        Returns
        -------
        Any
            The user-defined section state.
        '''
        return self.dict[module]['sections'][section]['state']
    
    @staticmethod
    def _get_location(frame):
        module = inspect.getmodule(frame)
        module = module.__name__ if module is not None else '__main__'
        section = inspect.getframeinfo(frame).function
        return module, section

    def get_namespace(self, module:str=None, section:str=None):
        '''
        Get the namespace inside the section.

        Parameters
        ----------
        module : str, optional
            The importable name of the module.
            If its None, it will get the current
            module
        section : str, optional
            The name of the generator function.
            If its None, the function will return 
            the module globals.

        Returns
        -------
        object
            The namespace required from the module or the section.
        '''
        
        if module is None:
            module = self._get_location(inspect.currentframe().f_back)[0]
        
        namespace = type('Namespace', (object,), {})()

        if section is None:
            namespace.__dict__ = self.dict[module]['ref'].__dict__
        else:
            frame = self.dict[module]['sections'][section]['generator'].gi_frame
            namespace.__dict__ = frame.f_locals
        
        return namespace

    def decorate_above(self, otype: type, decorator: Callable):
        '''
        Decorate every object above that is a otype 
        instance inside the actual section

        Parameters
        ----------
        otype : type
            The target object type.
        decorator : Callable
            The decorator that will be applied.
        '''
        nms = inspect.currentframe().f_back.f_locals
        for k, v in nms.items():
            if isinstance(v, otype):
                nms[k] = decorator(v)

    def from_folder(self, path:str, ignore:list=None, switch:int=1):
        '''
        Loads every extension that loader can find
        inside a folder, with relative import paths.

        Parameters
        ----------
        path : str
            The path to the folder.
        ignore : list, optional
            A list of extensions to be ignored.
        switch: int, optional
            Times the section state should be switched
            (per section).
        '''
        ignore = ignore or []
        if path not in sys.path:
            sys.path.insert(1, path)

        for x in os.listdir(path):
            hidden = x.startswith('__') and x.endswith('__')
            python = x.endswith('.py')
            if not hidden and python:
                x = x.rsplit('.py', 1)[0]
                if x not in ignore:
                    self.fully_load(x, switch=switch)
    
    def fully_load(self, *extensions, switch:int=1):
        '''
        Loads multiple extensions from a list
        of importable names.

        Parameters
        ----------
        *extensions 
            A list of importable names.
        switch: int
            Times the section state should be switched
            (per section).
        '''
        for x in extensions:
            self.add(x)
            for y in dir(self.dict[x]['ref']):
                self.load_section(x, y, switch=switch)

    def fully_reload(self, *extensions, new_switch:int=1):
        '''
        Reloads multiple extensions from a list
        of importable names.

        Parameters
        ----------
        *extensions 
            A list of importable names.
        new_switch: int
            Times the new sections states should be switched
            (per section).
        '''
        for k in extensions:
            v = self.dict[k]
            sections = [(k, v['state']) 
                        for k,v in v['sections'].items()]
            try:
                self.reload(k)
            except Exception as e:
                raise e
            finally:
                for x in sections:
                    self.load_section(k, x[0], switch=0)
                    self.switch_until_state(k, x[0], x[1])
                self.load_sections(k, switch=new_switch,
                                   exclude=sections)

def install(bot:kommando.KBot):
    '''
    Installs a Loader on the bot
    
    Parameters
    ----------
    bot : kommando.Kbot
        A kommando bot instance
    '''
    bot.loader = Loader(bot)

def watch(bot:kommando.KBot, wait=1):
    '''
    Installs a watcher on the bot loop
    
    Parameters
    ----------
    bot : kommando.Kbot
        A kommando bot instance
    '''
    async def watcher(self, wait=wait):
        dates = {}
        while True:
            for k,v in {**self.loader.dict}.items():
                f = v['ref'].__file__
                md = os.stat(f).st_mtime
                if f in dates:
                    if dates[f] < md:
                        try:
                            self.loader.fully_reload(k)
                        except:
                            traceback.print_exc()
                        finally:
                            dates[f] = md
                else:
                    dates[f] = md
            await asyncio.sleep(wait)
    bot.loop.create_task(watcher(bot))
