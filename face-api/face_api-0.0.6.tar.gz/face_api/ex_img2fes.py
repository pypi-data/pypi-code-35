# -*- coding: utf-8 -*-
# Face API example, convert face-image to 128 dim features vector (normalized to 1)
# BIG CHENG, init 2019/03/20
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
import click
import os
import sys
import numpy as np
import face_api


from face_api.cli2srv import cli2srv
import face_api.img_util as img_util
import face_api.file_util as file_util

@click.command()
#@click.argument('path_query_image', type=click.Path(exists=True))
@click.argument('path_query_image')

def main(path_query_image):

    img1 = img_util.file2img(path_query_image)
    print (img1.shape)

    if False:
        cli2srv1.server = "35.243.250.20:8500"
    else:
        cli2srv1.server = "127.0.0.1:8500"

    ## image to features
    fes1 = cli2srv().img2fes(img1)
    print (fes1)
    

if __name__ == "__main__":
    main()


"""

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
"""
