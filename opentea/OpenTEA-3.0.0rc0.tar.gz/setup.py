#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name="OpenTEA",
    version="3.0.0rc0",
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'example = opentea.gui.example:main',
        ],
    },
    # scripts=[
    #     'bin/opentea'
    # ],

    install_requires=[
        'numpy>=1.16.2',
        'h5py>=2.9.0',
        'jsonschema==2.6.0',
        'Pillow>=5.4.1',
        'PyYAML>=3.13',
    ],
    package_data={'opentea': ['gui_forms/images/*.gif']},
    # metadata
    author='Antoine Dauptain',
    author_email='coop@cerfacs.fr',
    description='Helpers tools for the setup of Scientific software',
    license="CeCILL-B",
    url='http://cerfacs.fr/opentea/',
)
