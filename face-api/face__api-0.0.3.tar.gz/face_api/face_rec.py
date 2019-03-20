# -*- coding: utf-8 -*-
# command for face recognition
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

@click.command()
@click.argument('known_people_folder')
@click.argument('image_to_check')
@click.option('--cpus', default=1, help='number of CPU cores to use in parallel (can speed up processing lots of images). -1 means "use all in system"')
@click.option('--tolerance', default=0.6, help='Tolerance for face comparisons. Default is 0.6. Lower this if you get multiple matches for the same person.')
@click.option('--show-distance', default=False, type=bool, help='Output face distance. Useful for tweaking tolerance setting.')
def main(known_people_folder, image_to_check, cpus, tolerance, show_distance):
    known_names, known_face_encodings = scan_known_people(known_people_folder)

    # Multi-core processing only supported on Python 3.4 or greater
    if (sys.version_info < (3, 4)) and cpus != 1:
        click.echo("WARNING: Multi-processing support requires Python 3.4 or greater. Falling back to single-threaded processing!")
        cpus = 1

    if os.path.isdir(image_to_check):
        if cpus == 1:
            click.echo("WARNING: Multi")
            #[test_image(image_file, known_names, known_face_encodings, tolerance, show_distance) for image_file in image_files_in_folder(image_to_check)]
        else:
            click.echo("WARNING: Multi")
            #process_images_in_process_pool(image_files_in_folder(image_to_check), known_names, known_face_encodings, cpus, tolerance, show_distance)
    else:
        click.echo("WARNING: Multi")
        #test_image(image_to_check, known_names, known_face_encodings, tolerance, show_distance)


if __name__ == "__main__":
    main()


"""
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
"""

