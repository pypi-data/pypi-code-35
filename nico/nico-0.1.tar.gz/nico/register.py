#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

from nico.consts import DEFAULT_TOPIC


class Register(object):

    registers = {}

    @classmethod
    def generate_key(cls, topic, message_type):
        return '{}:{}'.format(topic, message_type)

    def register(self, topic, message_type, func):
        key = self.generate_key(topic, message_type)
        if key not in self.registers:
            self.registers[key] = []
        self.registers[key].append(func)

    def get_jobs(self, topic, message_type):
        key = self.generate_key(topic, message_type)
        return self.registers[key] if key in self.registers else []


register = Register()


def on(message_type, topic=DEFAULT_TOPIC):
    def decorate(func):
        register.register(topic, message_type, func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorate
