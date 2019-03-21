# -*- coding: utf-8 -*-
# file utility
# BIG CHENG, init 2019/03/07
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
# ==============================================================================


from __future__ import print_function

import os
from glob import glob

def fname2path(path_root, fname):
  return os.path.join(path_root, fname)

def fnames2paths(path_root, fnames):
  return [os.path.join(path_root, fname) for fname in fnames]

def list_subdirs(path_root): ## similar to os.walk
  ## todo: check path_root
  paths = []
  for fname in sorted(os.listdir(path_root)):
    path = os.path.join(path_root, fname)
    if os.path.isdir(path):
        paths += [path]
            
  return paths
  
def list_files(path_root): ## similar to os.walk
  ## todo: check path_root
  paths = []
  for fname in sorted(os.listdir(path_root)):
    path = os.path.join(path_root, fname)
    if os.path.isfile(path):
        paths += [path]
            
  return paths


## naive local test
if __name__ == "__main__":

  def utest_list_subdirs():  
    print(list_subdirs(".."))
    
  
  utest_list_subdirs()
  



