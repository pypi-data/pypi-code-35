# -*- coding: utf-8 -*-
# Face API helper
# BIG CHENG, init 2019/03/25
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

msg_ex_gen_imgs = "ex_gen_imgs [path_to_download_images]"
msg_ex_img2fes = "ex_img2fes [face_cropped_image_to_query]"
msg_ex_imgs2conf_matrix = "ex_imgs2conf_matrix [face_cropped_images_to_compute_confusion_matrix]"
msgs = [msg_ex_gen_imgs, msg_ex_img2fes, msg_ex_imgs2conf_matrix]


@click.command()
def main():

    print("face api commands:")
    for msg in msgs:
        print("\t"+msg)
    

if __name__ == "__main__":
    main()
