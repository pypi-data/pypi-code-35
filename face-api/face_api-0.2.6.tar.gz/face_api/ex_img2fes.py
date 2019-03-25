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

from face_api.grpc_cli import grpc_cli
import face_api.img_util as img_util

@click.command()
@click.argument('path_query_image')

def main(path_query_image):

    ## load image
    img1 = img_util.file2img(path_query_image)
    print (img1.shape)

    ## image to features
    fes1 = grpc_cli().img2fes(img1)
    print (fes1)
    

if __name__ == "__main__":
    main()



