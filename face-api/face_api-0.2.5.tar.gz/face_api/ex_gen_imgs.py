# -*- coding: utf-8 -*-
# Generate images for Face API example running
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
import os
import shutil

def cp_files(src, dst):
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, dst)
        
@click.command()
@click.argument('path2download')

def main(path2download):

    ## copy images
    print (os.getcwd())
    path_script = os.path.abspath(__file__)
    path_base = os.path.dirname(path_script)
    print (path_base)
    path_imgs = os.path.join(path_base, "imgs")
    cp_files(path_imgs, path2download)


if __name__ == "__main__":
    main()



