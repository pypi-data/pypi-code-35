# Copyright 2019 HMS Industrial Networks AB
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

from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(name="hms-abcc40",
      version="0.0.1",
      description="Anybus CompactCom40 access via REST",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="HMS Industrial Networks AB",
      author_email="pythoncontact@hms.se",
      url="https://github.com/hms-networks/hms-abcc40",
      packages=find_packages(),
      classifiers=[
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Operating System :: OS Independent",
          ],
      )
