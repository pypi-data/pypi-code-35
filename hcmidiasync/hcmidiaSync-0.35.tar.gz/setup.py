# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='hcmidiaSync',
    version='0.35',
    url='https://temoque.com.br/',
    license='MIT License',
    author='Carla Dias',
    author_email='carladias@temoque.com.br',
    keywords='sync videos screenly',
    description=u'Sync videos',
    packages=['hcmidiaSync'],
    py_modules=["sync, host, hcmidia_host"],
    scripts=['hcmidiaSync/bin/hcmidia-sync', 'hcmidiaSync/bin/hcmidia-schedule', 'hcmidiaSync/bin/hcmidia-clean'],
    install_requires=['requests', 'simplejson'],
)