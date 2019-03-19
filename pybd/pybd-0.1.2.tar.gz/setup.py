# Copyright 2019 John T. Foster
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools

from pybd import __version__

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybd",
    version=__version__,
    author="John T. Foster",
    author_email="johntfoster@daytum.org",
    description="A Python API for accessing the Bazean database",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/daytum/PyBD",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy", "psycopg2-binary", "pandas"],
)
