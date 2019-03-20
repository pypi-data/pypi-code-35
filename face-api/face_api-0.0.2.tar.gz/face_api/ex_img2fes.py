# -*- coding: utf-8 -*-
# Frapi example, convert face-image to 128 dim features vector (normalized to 1)

# BIG CHENG, init 2019/03/07

import numpy as np
import frapi

from frapi.cli2srv import cli2srv
import frapi.img_util as img_util
import frapi.file_util as file_util

## load image
img1 = img_util.file2img("../imgs/coco1.png")
print (img1.shape)

## image to features
cli2srv1 = cli2srv()
cli2srv1.model = "mnet1" ## or fnet1
cli2srv1.signature = "mnet1_signature" # the same as fnet
if True:
    cli2srv1.server = "35.243.250.20:8500"
else:
    cli2srv1.server = "127.0.0.1:8500"

fes1 = cli2srv1.img2fes(img1)
print (fes1)



