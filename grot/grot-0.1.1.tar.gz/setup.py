# -*- coding: utf8
from setuptools import setup

with open("README.rst") as f:
    long_description = f.read()

with open('requirements.txt') as f:
    lines = [line.strip() for line in f.readlines() if line]
    required = [line for line in lines if not line.startswith('#') and not line.startswith('-i')]

setup(
    name='grot',
    version='0.1.1',
    author='Michal Kaczmarczyk',
    author_email='michal.s.kaczmarczyk@gmail.com',
    maintainer='Michal Kaczmarczyk',
    maintainer_email='michal.s.kaczmarczyk@gmail.com',
    license='MIT license',
    url='https://gitlab.com/kamichal/grot',
    description='Graphviz syntax wrapper. Draw graphs with pure python.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    packages=['grot'],
    install_requires=required,
    keywords='',
    classifiers=[
        # https://pypi.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Utilities',
    ],
)
