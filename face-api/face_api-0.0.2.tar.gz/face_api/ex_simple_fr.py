# -*- coding: utf-8 -*-
# Frapi example, compare the similarity of two face-image.
# each face-image is turned to 128 dim features vector (normalized to 1)
# then get the similairty by simply inner produciton.

# BIG CHENG, init 2019/03/07

import numpy as np
import frapi
import frapi.cli2srv as cli2srv
import frapi.img_util as img_util
import frapi.file_util as file_util
import frapi.math_helper as math_helper

## change server if need
if True: ## mnet1
  cli2srv._env.server = "127.0.0.1:8600"
  cli2srv._env.model = "mnet1"

names = ["coco"]*2 + ["nicole"]*2
path_imgs = file_util.fnames2paths("../imgs",  ["coco1.png", "coco7.png", "nicole1.png", "nicole7.png"])
imgs = img_util.files2imgs(path_imgs)
fess = cli2srv.imgs2fess(imgs)

# show similarity
print()
for i in range(len(names)-1):
  print ("%s vs %s: %f" % (names[i], names[i+1], math_helper.fes2sim(fess[i], fess[i+1])))
"""
print ("coco vs coco: %f" % math_helper.fes2sim(fes_c1, fes_c7))  # show be larger (>0.6)
print ("coco vs nicole: %f" % math_helper.fes2sim(fes_c1, fes_n1))  # show be smaller (<0.5)
print ("nicole vs nicole: %f" % math_helper.fes2sim(fes_n1, fes_n7))  # show be larger (>0.6)
"""
