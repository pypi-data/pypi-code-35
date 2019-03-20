# -*- coding: utf-8 -*-
# Frapi example for simple face detection

# BIG CHENG, init 2019/03/08

import numpy as np
import frapi.file_util as file_util
import frapi.fd_facade as fd
#import frapi.cli2srv as cli2srv
from frapi.cli2srv import cli2srv
import frapi.math_helper as math_helper
#import frapi.fr_facade as fr

## init fd-obj
fd1 = fd.fd_facade()

## prep
path_imgs = file_util.fnames2paths("../imgs", ["ka26.png", "ka27.png", "na199.png", "na200.png"])
print(path_imgs)
n_img = len(path_imgs)
names = ["ka"]*2 + ["na"]*2

## detect faces in an image
imgs = []
for i in range(n_img):
  crops = fd1.file2crops(path_imgs[i])
  print (len(crops))  ## in this example, should be 1
  #for j in range(len(crops)):
  #  print (crops[j].shape)
  imgs += [crops[0]]

## convert to np-array
imgs = np.array(imgs)
print (imgs.shape)


## image to features
cli1 = cli2srv()
if False: ## mnet1
  cli1.server = "127.0.0.1:8600"
  cli1.model = "mnet1"
    
fess = cli1.imgs2fess(imgs)

## calculate confusion matrix
cm = math_helper.fess2confusion(fess)
print (cm)

## init fr-obj
#fr1 = fr.fr_facade()

## register images & names
#fr1.imgs2reg(imgs, names)

## query image to check which face similar
#path_infs = file_util.fnames2paths("../imgs", ["ka28.png", "na201.png"])
#for i in range(len(path_infs)):
#  print(fr1.file2inf(path_infs[i]))


