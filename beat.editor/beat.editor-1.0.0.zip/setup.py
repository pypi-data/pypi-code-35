#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2016 Idiap Research Institute, http://www.idiap.ch/           #
# Contact: beat.support@idiap.ch                                              #
#                                                                             #
# This file is part of the beat.editor module of the BEAT platform.             #
#                                                                             #
# Commercial License Usage                                                    #
# Licensees holding valid commercial BEAT licenses may use this file in       #
# accordance with the terms contained in a written agreement between you      #
# and Idiap. For further information contact tto@idiap.ch                     #
#                                                                             #
# Alternatively, this file may be used under the terms of the GNU Affero      #
# Public License version 3 as published by the Free Software and appearing    #
# in the file LICENSE.AGPL included in the packaging of this file.            #
# The BEAT platform is distributed in the hope that it will be useful, but    #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY  #
# or FITNESS FOR A PARTICULAR PURPOSE.                                        #
#                                                                             #
# You should have received a copy of the GNU Affero Public License along      #
# with the BEAT platform. If not, see http://www.gnu.org/licenses/.           #
#                                                                             #
###############################################################################


from setuptools import setup, find_packages, dist
dist.Distribution(dict(setup_requires=['beat.cmdline']))

def load_requirements(f):
  retval = [str(k.strip()) for k in open(f, 'rt')]
  return [k for k in retval if k and k[0] not in ('#', '-')]

# The only thing we do in this file is to call the setup() function with all
# parameters that define our package.
setup(

    name='beat.editor',
    version=open("version.txt").read().rstrip(),
    description='Local editor for BEAT objects',
    url='https://gitlab.idiap.ch/beat/beat.editor',
    license='AGPLv3',
    author='Idiap Research Institute',
    author_email='beat.support@idiap.ch',
    long_description=open('README.rst').read(),

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=load_requirements('requirements.txt'),
    entry_points={
        # main entry for beat editor cli
        'beat.cli': [
            'editor = beat.editor.scripts.server_cli:editor',
        ],
        'beat.editor.cli': [
            'serve = beat.editor.scripts.server_cli:serve',
        ],

    },

    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
