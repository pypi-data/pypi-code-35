# coding=utf-8
# Copyright 2019 The TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""Generate fake data for cats_vs_dogs dataset.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import zipfile

from absl import app
from absl import flags

from tensorflow_datasets.core.utils import py_utils
from tensorflow_datasets.testing import fake_data_utils

flags.DEFINE_string('tfds_dir', py_utils.tfds_dir(),
                    'Path to tensorflow_datasets directory')

FLAGS = flags.FLAGS


def _output_dir():
  return os.path.join(FLAGS.tfds_dir, 'testing', 'test_data', 'fake_examples',
                      'cats_vs_dogs')


def main(argv):
  del argv
  out_path = os.path.join(_output_dir(), 'cats_vs_dogs.zip')
  jpg = fake_data_utils.get_random_jpeg(height=1, width=1)
  with zipfile.ZipFile(out_path, 'w') as myzip:
    myzip.write(jpg, 'PetImages/Dog/0.jpg')
    myzip.write(jpg, 'PetImages/Dog/1.jpg')
    myzip.write(jpg, 'PetImages/Cat/0.jpg')
    myzip.write(jpg, 'PetImages/Cat/1.jpg')


if __name__ == '__main__':
  app.run(main)
