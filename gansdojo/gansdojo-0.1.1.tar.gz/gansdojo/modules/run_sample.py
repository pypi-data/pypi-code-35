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
from tensorflow.keras import backend as K

from gansdojo import ObservableDojo

class SampleRunner:
    """Run sample and save them to summary regularly."""

    def __init__(self, interval_in_steps=50):
        self.interval = interval_in_steps

    def setup(self, observable:ObservableDojo):
        observable.register('after_train_step', self.run)
        self._observable = observable

    def run(self, loss_d, loss_g, epoch, iteration, *args, **kwargs):
        generated = self._observable.run()
        generated = (generated + 1.0) / 2.0
        tf.contrib.summary.image('generated', K.expand_dims(K.concatenate(generated, axis=1), axis=0))
        
