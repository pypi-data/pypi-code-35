# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(THIS_DIR, "README.rst")) as f:
    long_description = f.read()

with open('requirements.txt') as f:
    lines = [line.strip() for line in f.readlines() if line]
    required = [line for line in lines if not line.startswith('#') and not line.startswith('-i')]

setup(
    name='xslide',
    version='0.1',
    author='Michał Kaczmarczyk',
    author_email='michal.s.kaczmarczyk@gmail.com',
    maintainer='Michał Kaczmarczyk',
    maintainer_email='michal.s.kaczmarczyk@gmail.com',
    license='MIT license',
    url='https://gitlab.com/kamichal/xslide',
    description='',
    long_description=long_description,
    long_description_content_type='text/x-rst; charset=UTF-8',
    packages=find_packages(),
    requires=[],
    install_requires=required,
    keywords='',
    classifiers=[
        # https://pypi.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Multimedia :: Graphics :: Presentation',
    ],
    entry_points={
        'console_scripts': [
            'serve_slides = xslide.serve_slides:main',
        ],
    },
    include_package_data=True,
)
