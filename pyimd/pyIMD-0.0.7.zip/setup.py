# /********************************************************************************
# * Copyright © 2018-2019, ETH Zurich, D-BSSE, Andreas P. Cuny & Gotthold Fläschner
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the GNU Public License v3.0
# * which accompanies this distribution, and is available at
# * http://www.gnu.org/licenses/gpl
# *
# * Contributors:
# *     Andreas P. Cuny - initial API and implementation
# *******************************************************************************/

from setuptools import setup


def extract_version():
    """
    Return pyIMD.__version__ from pyIMD/__init__.py
    """
    with open('pyIMD/__init__.py') as fd:
        ns = {}
        for line in fd:
            if line.startswith('__version__'):
                exec(line.strip(), ns)
                return ns['__version__']


setup(name='pyIMD',
      version=extract_version(),
      author='Andreas P. Cuny <andreas.cuny@bsse.ethz.ch>, Gotthold Fläschner <gotthold.flaeschner@bsse.ethz.ch>',
      author_email="andreas.cuny@bsse.ethz.ch",
      url='https://gitlab.com/csb.ethz/pyIMD/tree/master',
      download_url='https://gitlab.com/csb.ethz/pyIMD/tree/master',
      description='Inertial mass determination',
      long_description='',
      packages={'pyIMD': 'pyIMD',
                'pyIMD.analysis': 'pyIMD/analysis',
                'pyIMD.configuration': 'pyIMD/configuration',
                'pyIMD.error': 'pyIMD/error',
                'pyIMD.examples': 'pyIMD/examples',
                'pyIMD.io': 'pyIMD/io',
                'pyIMD.plotting': 'pyIMD/plotting',
                'pyIMD.tests': 'pyIMD/tests',
                'pyIMD.ui': 'pyIMD/ui'},
      package_dir={'pyIMD': 'pyIMD',
                   'pyIMD.analysis': 'pyIMD/analysis',
                   'pyIMD.configuration': 'pyIMD/configuration',
                   'pyIMD.error': 'pyIMD/error',
                   'pyIMD.examples': 'pyIMD/examples',
                   'pyIMD.io': 'pyIMD/io',
                   'pyIMD.plotting': 'pyIMD/plotting',
                   'pyIMD.tests': 'pyIMD/tests',
                   'pyIMD.ui': 'pyIMD/ui'},
      keywords='Inertial mass determination',
      license='GPL3.0',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Science/Research',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: Microsoft :: Windows :: Windows 7',
                   'Programming Language :: Python :: 3',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Topic :: Scientific/Engineering'
                   ],
      install_requires=['pandas==0.23.3', 'numpy==1.14.5', 'scipy==1.1.0', 'nptdms==0.12.0', 'tqdm==4.23.4',
                        'plotnine==0.3.0', 'PyQT5', 'lxml', 'xmltodict', 'matplotlib', 'pyyaml', 'pyqtgraph',
                        'xmlunittest'],

      )
