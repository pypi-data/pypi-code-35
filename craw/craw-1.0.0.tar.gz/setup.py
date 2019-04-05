# -*- coding: utf-8 -*-

###########################################################################
#                                                                         #
# This file is part of Counter RNAseq Window (craw) package.              #
#                                                                         #
#    Authors: Bertrand Neron                                              #
#    Copyright (c) 2017-2019  Institut Pasteur (Paris).                   #
#    see COPYRIGHT file for details.                                      #
#                                                                         #
#    craw is free software: you can redistribute it and/or modify         #
#    it under the terms of the GNU General Public License as published by #
#    the Free Software Foundation, either version 3 of the License, or    #
#    (at your option) any later version.                                  #
#                                                                         #
#    craw is distributed in the hope that it will be useful,              #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of       #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                 #
#    See the GNU General Public License for more details.                 #
#                                                                         #
#    You should have received a copy of the GNU General Public License    #
#    along with craw (see COPYING file).                                  #
#    If not, see <http://www.gnu.org/licenses/>.                          #
#                                                                         #
###########################################################################

import os
import sysconfig

from setuptools import setup, find_packages
from setuptools.dist import Distribution

from craw import __version__ as cr_vers


class UsageDistribution(Distribution):

    def __init__(self, attrs=None):
        # It's important to define options before to call __init__
        # otherwise AttributeError: UsageDistribution instance has no attribute 'conf_files'
        self.fix_lib = None
        Distribution.__init__(self, attrs=attrs)
        self.common_usage = """\
Common commands: (see '--help-commands' for more)

  setup.py build      will build the package underneath 'build/'
  setup.py install    will install the package
  setup.py test       run tests after in-place build
"""


def get_install_data_dir(inst):
    """
    :param inst: installation option
    :type inst: dict
    :return: the prefix where to install data
    :rtype: string
    """

    if 'VIRTUAL_ENV' in os.environ:
        inst['prefix'] = ('environment', os.environ['VIRTUAL_ENV'])
    elif 'user' in inst:
        import site
        inst['prefix'] = ('command line', site.USER_BASE)
    elif 'root' in inst:
        inst['prefix'] = ('command line',
                          os.path.join(inst['root'][1],
                                       sysconfig.get_path('data').strip(os.path.sep)
                                       )
                          )

    if 'install_data' in inst:
        install_dir = inst['install_data'][1]
    elif 'prefix' in inst:
        install_dir = os.path.join(inst['prefix'][1], 'share')
    else:
        install_dir = os.path.join(sysconfig.get_path('data'), 'share')
    return install_dir


def expand_data(data_to_expand):
    """
    From data structure like setup.py data_files (see http://)
     [(directory/where/to/copy/the/file, [path/to/file/in/archive/file1, ...]), ...]
    but instead of the original struct this one accept to specify a directory in elements to copy.

    This function will generate one entry for all *content* of the directory and subdirectory
    recursively, to in fine copy the tree in archive in dest on the host

    the first level of directory itself is not include (which allow to rename it)
    :param data_to_expand:
    :type  data_to_expand: list of tuple
    :return: list of tuple
    """
    def remove_prefix(prefix, path):
        prefix = os.path.normpath(prefix)
        path = os.path.normpath(path)
        to_remove = len([i for i in prefix.split(os.path.sep) if i])
        truncated = [i for i in path.split(os.path.sep) if i][to_remove:]
        truncated = os.path.sep.join(truncated)
        return truncated

    data_struct = []
    for base_dest_dir, src in data_to_expand:
        base_dest_dir = os.path.normpath(base_dest_dir)
        for one_src in src:
            if os.path.isdir(one_src):
                for path, _, files in os.walk(one_src):
                    if not files:
                        continue
                    path_2_create = remove_prefix(one_src, path)
                    data_struct.append(
                        (os.path.join(base_dest_dir, path_2_create), [os.path.join(path, f) for f in files]))
            if os.path.isfile(one_src):
                data_struct.append((base_dest_dir, [one_src]))
    return data_struct


def read_md(f): return open(f, 'r').read()


setup(name="craw",
      version=cr_vers,
      author='Bertrand Neron',
      author_email='bneron@pasteur.fr',
      url="https://gitlab.pasteur.fr/bneron/craw",
      keywords=['bioinformatics', 'RNAseq', 'coverage'],
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        ],
      description="Counter RNA seq Window is a package which aim to compute and "
                  "visualize the coverage of RNA seq experiment.",
      long_description=read_md('README.md'),
      long_description_content_type='text/markdown',
      platforms=["Unix"],
      python_requires='>=3.5',
      install_requires=open("requirements.txt").read().split(),
      extras_require={'dev': open("requirements_dev.txt").read().split()},
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'craw_coverage=craw.scripts.craw_coverage:main',
              'craw_htmp=craw.scripts.craw_htmp:main',
          ]
      },

      data_files=expand_data([('share/craw/doc/html', ['doc/build/html/']),
                              ('share/craw/doc/pdf/', ['doc/build/latex/CounterRNAseqWindow.pdf'])]),

      distclass=UsageDistribution
      )
