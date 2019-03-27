# -*- coding:utf-8 -*-
import os, copy

class Mode:

    GLOBAL_DATA = {}

    def __init__(self):
        self._commands = {}
        self._after_command_messages = {}
        self._free_input_func = None
        self._after_free_input_message_func = None

        for name, method in self.__class__.__dict__.items():
            if hasattr(method, 'command_code'):
                for code in method.command_code:
                    self._commands[code] = method
            elif hasattr(method, 'after_command_message_code'):
                for code in method.after_command_message_code:
                    self._after_command_messages[code] = method
            elif hasattr(method, 'free_input_flg'):
                self._free_input_func = method
            elif hasattr(method, 'after_free_input_message_flg'):
                self._after_free_input_message_func = method

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

    def after_message(self, command):
        if command in self._after_command_messages:
            return self._after_command_messages[command](self)
        elif self._after_free_input_message_func:
            return self._after_free_input_message_func(self, command)
        else:
            return []

    def command(code):
        code_ = _convert_code2tuple(code)
        def add_attribute(func):
            func.command_code = code_
            return func
        return add_attribute

    def after_command_message(code):
        code_ = _convert_code2tuple(code)
        def add_attribute(func):
            func.after_command_message_code = code_
            return func
        return add_attribute

    def free_input(func):
        func.free_input_flg = True
        return func

    def after_free_input_message(func):
        func.after_free_input_message_flg = True
        return func


def _convert_code2tuple(code):
    if type(code) is str:
        return ([code])
    elif type(code) is tuple:
        return code
    else:
        raise Exception('Command words must be str or tuple.')

def set_global(name, obj):
    Mode.GLOBAL_DATA[name] = obj

def get_global(name):
    if name in Mode.GLOBAL_DATA:
        return copy.deepcopy(Mode.GLOBAL_DATA[name])
    else:
        return None

def reset_global():
    Mode.GLOBAL_DATA = {}

def start(initial_mode_cls):
    mode = initial_mode_cls()
    while True:
        next_mode_cls = mode_cycle(mode)
        del(mode)
        mode = next_mode_cls()

def mode_cycle(mode):
    mode.preprocess()
    premessage = mode.premessage()
    if premessage:
        print(os.linesep.join(premessage))
    command = mode.wait_command()
    next_mode_cls = mode.execute(command)
    after_message = mode.after_message(command)
    if after_message:
        print(os.linesep.join(after_message))
    return next_mode_cls