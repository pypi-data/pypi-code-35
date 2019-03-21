# -*- coding: utf-8 -*-
# Face API example, calculation confusion matrix from images.
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
import numpy as np
import face_api

from face_api.grpc_cli import grpc_cli
import face_api.img_util as img_util
import face_api.math_helper as math_helper
import click

@click.command()
@click.argument('path_query_images', nargs=-1)

def main(path_query_images):

    ## load images
    imgs = img_util.files2imgs(path_query_images)
    print (imgs.shape)

    ## image to features
    fess = grpc_cli().imgs2fess(imgs)

    ## calculate confusion matrix
    cm = math_helper.fess2confusion(fess)
    print (cm)
    

if __name__ == "__main__":
    main()


