# -*- coding:utf-8 -*-
import os

class Mode:

    GLOBAL_DATA = {}

    def __init__(self):
        self._commands = {}
        self._free_input_func = None

        for name, method in self.__class__.__dict__.items():
            if hasattr(method, 'command_code'):
                self._commands[method.command_code] = method
            elif hasattr(method, 'free_input_flg'):
                self._free_input_func = method

    def preprocess(self):
        """ abstruct method """
        pass

    def premessage(self):
        """ abstruct method """
        return []

    def command_message(self):
        """ abstruct method """
        return '>>> '

    def wait_command(self):
        return input(self.command_message()).strip()

    def execute(self, command):
        if command in self._commands:
            return self._commands[command](self)
        elif self._free_input_func:
            return self._free_input_func(self, command)
        else:
            return self.__class__

    def command(code):
        def add_attribute(func):
            func.command_code = code
            return func
        return add_attribute

    def free_input(func):
        func.free_input_flg = True
        return func

def set_global(name, obj):
    Mode.GLOBAL_DATA[name] = obj

def get_global(name):
    if name in Mode.GLOBAL_DATA:
        return Mode.GLOBAL_DATA[name]
    else:
        return None

def reset_global():
    Mode.GLOBAL_DATA = {}

def start(initial_mode_cls):
    mode = initial_mode_cls()
    while True:
        next_mode_cls = mode_cycle(mode)
        mode = next_mode_cls()

def mode_cycle(mode):
    mode.preprocess()
    premessage = mode.premessage()
    if premessage:
        print(os.linesep.join(premessage))
    command = mode.wait_command()
    next_mode_cls = mode.execute(command)
    return next_mode_cls
