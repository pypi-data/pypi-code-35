# -*- coding: utf-8 -*-
# Frapi example for simple face detection

# BIG CHENG, init 2019/03/08

import numpy as np
import frapi.fd_facade as fd
import frapi.file_util as file_util

## init fd-obj
fd1 = fd.fd_facade()

## detect faces in an image
path_img = file_util.fname2path("../imgs", "ka26.png")
print(fd1.file2dets(path_img))


