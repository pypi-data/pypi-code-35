# -*- coding: utf-8 -*-
# Facade interface for Face Recognition
# BIG CHENG, init 2019/03/08
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

import numpy as np
#import frapi
import frapi.cli2srv as cli2srv
import frapi.img_util as img_util
import frapi.math_helper as math_helper
import frapi.file_util as file_util

def file2fes(fname):
  ## todo: check fname
  img = img_util.file2img(fname)
  fes = cli2srv.img2fes(img)
  return fes
  
class fr_facade:
  
  def __init__(self):
    self.fess_reg = None
    self.names_reg = None
    if False: ## mnet1
      cli2srv._env.server = "127.0.0.1:8600"
      cli2srv._env.model = "mnet1"
      
  def files2reg(self, fnames, names):
    ## todo: check fnames, names ...
    imgs = img_util.files2imgs(fnames)
    #print (imgs.shape)
    self.names_reg = names
    self.fess_reg = cli2srv.imgs2fess(imgs)

  ## ref. to files2reg
  def imgs2reg(self, imgs, names):
    #print (imgs.shape)
    ## todo: check imgs shape, names ...
    self.names_reg = names
    self.fess_reg = cli2srv.imgs2fess(imgs)
    
  #todo:
  #def dir2reg():

  def file2inf(self, fname):
    ## todo: check fname
    fes = file2fes(fname)
    idx, sim = math_helper.find_max_sim(fes, self.fess_reg)
    ## todo: check idx
    return self.names_reg[idx], sim
    


