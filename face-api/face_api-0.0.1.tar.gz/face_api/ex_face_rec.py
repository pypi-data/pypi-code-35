# -*- coding: utf-8 -*-
# Frapi example for face recognition

# BIG CHENG, init 2019/03/07

import numpy as np
import frapi.fr_facade as fr
import frapi.file_util as file_util

## init fr-obj
fr1 = fr.fr_facade()

## register images & names
#fname_imgs = ["coco1.png", "nicole1.png"]
dir_base = "../imgs"
path_imgs = file_util.fnames2paths(dir_base, ["coco1.png", "nicole1.png"])
names = ["coco"] + ["nicole"]
fr1.files2reg(path_imgs, names)

## query image to check which face similar
path_infs = file_util.fnames2paths(dir_base, ["coco7.png", "nicole7.png"])
for i in range(len(path_infs)):
  print(fr1.file2inf(path_infs[i]))


