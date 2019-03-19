# MIT License
# 
# Copyright (c) 2019 Bowie
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 

import unittest
from tensorflow.keras import backend as K

class MockObserableDojo:

    def __init__(self, test_case:unittest.TestCase, config):
        self.test_case = test_case
        self.generator = config.generator()
        self.discriminator = config.discriminator()
        self.optimizer_generator = config.optimizer_generator
        self.optimizer_discriminator = config.optimizer_discriminator
        self.handlers = {}

    def register(self, event_name, handler):
        self.handlers[event_name] = handler

    def fire(self, name, *args, **kwargs):
        handler = self.handlers[name]
        handler(*args, **kwargs)

    def run(self, batch_size=4):
        return K.random_normal([batch_size, 3, 3, 3])
