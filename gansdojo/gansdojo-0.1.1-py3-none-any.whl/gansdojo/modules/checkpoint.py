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

from gansdojo import ObservableDojo

class CheckpointSaver:

    def __init__(self, save_dir, remove_old_data=False, auto_restore_latest=False):
        if remove_old_data and os.path.exists(save_dir):
            shutil.rmtree(save_dir)

        self.save_dir = save_dir
        self.auto_restore_lastest = auto_restore_latest

    def setup(self, observable:ObservableDojo):
        self.checkpoint_generator = tf.train.Checkpoint(
            optimizer=observable.optimizer_generator,
            model=observable.generator)
        self.checkpoint_discriminator = tf.train.Checkpoint(
            optimizer=observable.optimizer_discriminator,
            model=observable.discriminator)

        observable.register('after_epoch', self.save)

    def save(self, *args, **kwargs):
        # Create checkpoints
        self.checkpoint_generator.save(os.path.join(self.save_dir, 'generator', 'gen'))
        self.checkpoint_discriminator.save(os.path.join(self.save_dir, 'discriminator', 'dis'))
        
        # Persistent the global steps
        with open(os.path.join(self.save_dir, 'global_step.txt'), 'w') as fd:
            fd.write(str(tf.train.get_global_step().numpy()))