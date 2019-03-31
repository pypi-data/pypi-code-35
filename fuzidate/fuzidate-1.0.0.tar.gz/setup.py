# Copyright 2019 Rafe Kaplan
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

import sys

import setuptools

__version__ = '1.0.0'

description = """\
Fuzidate is a type used to represent information where the precise date may or
may not be known. While similar to a date range (defined as a tuple containing
a low date and a high date), it encodes information about at what level of
precision a date is not known.
"""

if sys.version_info < (3, 5):
    sys.exit('fuzidate requires Python 3.5 or greater')

setuptools.setup(
    name='fuzidate',
    version=__version__,
    license='Apache License 2.0',
    description='Representation of dates with limited precision.',
    long_description=description,
    author='Rafe Kaplan',
    url='https://github.com/slobberchops/fuzidate',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Sociology',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
