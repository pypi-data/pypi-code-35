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
from time import time

from gansdojo import ObservableDojo

class ConsoleUpdator:

    def before_batch_step(self, *args, **kwargs):
        self.begin = time()

    def after_batch_step(self, loss_g, loss_d, epoch, iteration, *args, **kwargs):
        speed = 1.0 / (time() - self.begin)
        global_step = tf.train.get_global_step().numpy()
        print((f'\r{global_step} E:{epoch} I:{iteration} {speed:.2f} b/s '
                f'G:{loss_g.numpy():.4e} D:{loss_d.numpy():.4e}'), end='')

    def setup(self, observable:ObservableDojo):
        observable.register('before_train_step', self.before_batch_step)
        observable.register('after_train_step', self.after_batch_step)