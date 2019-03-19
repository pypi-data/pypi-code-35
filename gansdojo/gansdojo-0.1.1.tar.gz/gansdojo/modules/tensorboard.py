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
import os
import shutil

class TensorBoardLogger:

    def __init__(self, log_dir, writer=None, remove_old_data=False):
        if remove_old_data and os.path.exists(log_dir):
            shutil.rmtree(log_dir)
        
        if writer is None:
            self._writer = tf.contrib.summary.create_file_writer(log_dir, flush_millis=1000)
            self._writer.set_as_default()
        else:
            self._writer = writer

    def after_train_batch(self, loss_g, loss_d, *args, **kwargs):
        tf.contrib.summary.scalar('loss_g', loss_g, family='loss')
        tf.contrib.summary.scalar('loss_d', loss_d, family='loss')

    def setup(self, dojo):
        dojo.register('after_train_step', self.after_train_batch)