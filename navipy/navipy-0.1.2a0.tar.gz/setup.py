#!/usr/bin/env python
""" setup.py for Insect Navigation Toolbox
(called navipy)
"""
from setuptools import setup, find_packages
import glob
import os

excluded = []


def exclude_package(pkg):
    for exclude in excluded:
        if pkg.startswith(exclude):
            return True
    return False


def create_package_list(base_package):
    return ([base_package] +
            [base_package + '.' + pkg
             for pkg
             in find_packages(base_package)
             if not exclude_package(pkg)])


def package_data_files(base_package):
    os.chdir(base_package)
    filelist = glob.glob(os.path.join('resources',
                                      '*'))
    filelist.extend(glob.glob(os.path.join('resources',
                                           '**', '*'),
                              recursive=True))
    os.chdir('../')
    print(filelist)
    return filelist


setup_dict = {'name': 'navipy',
              'version': '0.1.2a',
              'author': "Olivier J.N. Bertrand",
              'author_email': 'olivier.bertrand@uni-bielefeld.de',
              'description': 'Insect Navigation Toolbox',
              'packages': create_package_list("navipy"),
              'url': "https://gitlab.ub.uni-bielefeld.de/olivier.bertrand/navipy.git",
              'download_url': 'https://gitlab.ub.uni-bielefeld.de/olivier.bertrand/navipy/-/archive/v_012a/navipy-v_012a.tar.gz',
              'requires': ['numpy',
                           'pandas',
                           'matplotlib',
                           'scipy',
                           'networkx',
                           'ipython',
                           'yaml',
                           'PIL',
                           'cv2',
                           'fastdtw'],
              'install_requires': ["numpy",
                                   'pandas',
                                   'matplotlib',
                                   'scipy',
                                   'sphinx_rtd_theme',
                                   'networkx',
                                   'sphinx-argparse',
                                   'ipython',
                                   'flake8',
                                   'tox',
                                   'pyyaml',
                                   'Pillow',
                                   'tables',
                                   'nbsphinx',
                                   'opencv-python',
                                   'coverage',
                                   'fastdtw'],
              'package_data': {'navipy':
                               package_data_files("navipy")},
              'include_package_data': True,
              'entry_points': {
                  'console_scripts': [
                      'blendnavipy=navipy.scripts.blendnavipy:main',
                      'blendunittest=navipy.scripts.blendunittest:main',
                      'blendongrid=navipy.scripts.blend_ongrid:main',
                      'blendoverlaytraj=navipy.scripts.blend_overlaytraj:main',
                      'blendalongtraj=navipy.scripts.blend_alongtraj:main',
                      'dltcalibrator=navipy.scripts.dlt_calibrator:main'
                  ]},
              }

setup(**setup_dict)
