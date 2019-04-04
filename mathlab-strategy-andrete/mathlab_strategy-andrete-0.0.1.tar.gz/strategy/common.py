from enum import Enum
from typing import Any, Type, List

from .singleton import Singleton


class Instruction():
    pass


class Instructions(Singleton):
    def __init__(self):
        self.instructions = []

    def add(self, instruction: Instruction):
        self.instructions.append(instruction)

    def get_all(self) -> list:
        return self.instructions

    def clear(self) -> None:
        self.instructions = []


class Values(Singleton):
    def __init__(self):
        self.values = {}

    def set(self, key, new):
        self.values[key] = new

    def get(self, key):
        return self.values[key]

    def contains(self, key):
        return key in self.values.keys()


class Value():
    def __init__(self, key: str):
        self.key = key
        if not Values().contains(key):
            Values().set(key, None)

    def set_value(self, value: Any):
        Values().set(self.key, value)

    def get_value(self):
        return Values().get(self.key)

    def get_key(self):
        return self.key

    def __add__(self, right: Any):
        return self.get_value() + right

    def __radd__(self, left: Any):
        return left + self.get_value()

    def __sub__(self, right: Any):
        return self.get_value() - right

    def __rsub__(self, left: Any):
        return left - self.get_value()

    def __lt__(self, right: Any):
        return self.get_value() < right

    def __gt__(self, right: Any):
        return self.get_value() > right

    def __eq__(self, right: Any):
        return self.get_value() == right

    def __str__(self):
        return self.get_value().__str__()


class Parameters(Singleton):
    def __init__(self):
        self.parameters = {}

    def set(self, name: str, value: Any):
        print(name, value)
        self.parameters[name] = value

    def get(self, name: str):
        return self.parameters[name]

    def contains(self, name: str):
        return name in self.parameters.keys()


class ParameterFunc():
    def __call__(self, name: str, cls: Type = str, default: Any = None):
        if Parameters().contains(name):
            return Parameters().get(name)
        else:
            return default


Parameter = ParameterFunc()


class StatusEnv(Singleton):
    def __init__(self):
        self.envs = {}

    def set(self, name, value):
        self.envs[name] = value

    def get(self, name):
        return self.envs.get(name)

    def contains(self, name):
        return name in self.envs.keys()


class Status():
    def __init__(self, name: str, enum: List[str], init: str):
        self.name = name
        if not StatusEnv().contains(self.name):
            StatusEnv().set(self.name, init)

    def __is__(self, s: str) -> bool:
        return self.get() == s

    def __ne__(self, s) -> bool:
        if isinstance(s, str):
            return self.get() != s
        return NotImplemented

    def __eq__(self, s) -> bool:
        if isinstance(s, str):
            return self.get() == s
        return NotImplemented

    def set(self, s: str):
        StatusEnv().set(self.name, s)

    def get(self):
        return StatusEnv().get(self.name)


class Interval(Enum):
    M1 = 'm1'
    M5 = 'm5'
    M10 = 'm10'
    M15 = 'm15'
    M30 = 'm30'
    Hour = 'h1'
    Day = 'day'
    Week = 'week'
