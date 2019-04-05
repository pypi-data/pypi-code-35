# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


version = '0.1.0'


setup(
    name='djangomix',
    version=version,
    keywords='Django Mix',
    description='Django integration for Laravel Mix',
    long_description=open('README.md').read(),

    url='https://github.com/m-a-k-o/django-mix',

    author='Marek Racik',
    author_email='marek@racik.info',

    packages=['django-mix'],
    py_modules=[],
    install_requires=[],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
