# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-ubigeo-peru',
    version='0.2.4',
    license='GPL v.3',
    description='''
        Django app para aplicaciones que requieran usar los ubigeos del Perú.
    ''',
    long_description=README,
    author='Miguel Angel Cumpa Asuña',
    author_email='miguel.cumpa.ascuna@gmail.com',
    url='https://bitbucket.org/micky_miseck/django-ubigeo-peru',
    download_url='https://bit.ly/2TmzzVB',
    keywords=['ubigeo', 'peru'],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    include_package_data=True,
    zip_safe=False,
)
