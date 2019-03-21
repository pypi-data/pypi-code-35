# -*- coding: utf-8 -*-
# Facade interface for Face Detection
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

import dlib
import numpy as np
#from scipy import misc
#from PIL import Image
import frapi.img_util as img_util

## convert dlib-rectangles to numpy matrix
def _rects2dets(rects):
  n_rect = len(rects)
  dets = np.zeros((n_rect, 4))
  for i in range(n_rect):
    d = rects[i]
    dets[i] = np.array([d.left(), d.top(), d.right(), d.bottom()])
  return dets

img_size = 160

class fd_facade:

  def __init__(self):
    self.detector = dlib.get_frontal_face_detector()

  def file2dets(self, fname):
    ## todo check 
    _, img = img_util._file2img(fname)
    
    #print (img.shape)
    rects = self.detector(img, 0)
    dets = _rects2dets(rects)
    return dets


  def file2crops(self, fname, for_fr=True):
    raw, img = img_util._file2img(fname)
    rects = self.detector(img, 0)
    dets = _rects2dets(rects)
    
    n_det = dets.shape[0]
    imgs_crop = []
    for i in range(n_det):
      raw_crop = raw.crop(dets[i])
      raw_crop = raw_crop.resize((img_size, img_size))
      raw_crop.save("%d.png" % i) ## debug
      img_crop = np.array(raw_crop)
      #print (img_crop.shape)
      if for_fr:
        img_crop = img_util._img2img4fr(img_crop)
      imgs_crop += [img_crop]
      
    return imgs_crop
      
  
"""
def run_crop_face():

    faces_folder_path = "coco1.png"
    detector = dlib.get_frontal_face_detector()
    f = faces_folder_path

    print("Processing file: {}".format(f))
    img = misc.imread(f)

    dets = detector(img, 0)
    print("Number of faces detected: {}".format(len(dets)))
    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
 
    #io.imsave(faces_result_path, img)
"""

## naive local test
if __name__ == "__main__":

  def utest_fd():
    fd1 = fd_dlib()
    #img = img_util.file2img("coco1.png")
    fd1.detect("coco1.png")

  #run_crop_face()
  utest_fd()

"""
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


  fr1 = fr_facade()
  
  def utest_reg():
    fname_imgs = ["coco1.png", "coco7.png", "nicole1.png", "nicole7.png"]
    names = ["coco"]*2 + ["nicole"]*2
    fr1.files2reg(fname_imgs, names)
    print (fr1.fess_reg.shape)

  def utest_inf():
    fname_imgs = ["coco1.png", "nicole1.png"]
    names = ["coco"] + ["nicole"]
    fr1.files2reg(fname_imgs, names)
    print(fr1.file2inf("coco7.png"))
    print(fr1.file2inf("nicole7.png"))
  
  #utest_reg()
  utest_inf()

"""    

