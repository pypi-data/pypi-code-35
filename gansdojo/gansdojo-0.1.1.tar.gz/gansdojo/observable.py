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

import tensorflow as tf

from .dojo import Dojo

class ObservableDojo(Dojo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__subjects = {}
        def add_subject(obj, name):
            value = Subject() 
            obj.__subjects[name] = value

        add_subject(self, 'before_initialization')
        add_subject(self, 'before_train_step')
        add_subject(self, 'after_train_step')
        add_subject(self, 'before_epoch')
        add_subject(self, 'after_epoch')

    def train_on_batch(self, *args, **kwargs):
        
        self.__subjects['before_train_step'].notify(*args, **kwargs) 

        loss_g, loss_d = super().train_on_batch(*args, **kwargs)

        self.__subjects['after_train_step'].notify(loss_g, loss_d, *args, **kwargs)

        return loss_g, loss_d

    def train_epoch(self, *args, **kwargs):
        self.__subjects['before_epoch'].notify(*args, **kwargs)
        super().train_epoch(*args, **kwargs)
        self.__subjects['after_epoch'].notify(*args, **kwargs)

    def train(self, *args, **kwargs):
        self.__subjects['before_initialization'].notify(*args, **kwargs)
        super().train(*args, **kwargs)

    def register(self, subject, observer):
        self.__subjects[subject].register(observer)


class Subject:

    def __init__(self):
        self.__observers = []

    def register(self, observer):
        self.__observers.append(observer)
    
    def notify(self, *args, **kwargs):
        for observer in self.__observers:
            observer(*args, **kwargs)