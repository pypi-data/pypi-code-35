# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.rst') as f:
    long_description = f.read()

setup(
    name='dj-admins-setting',
    version='1.0.0',
    url='https://github.com/hernantz/dj-admins-setting',
    license='BSD',
    author='Hernan Lozano',
    author_email='hernantz@gmail.com',
    description='Use a string to configure the admins '
                'emails setting in your Django Application.',
    long_description=long_description,
    py_modules=['dj_admins_setting'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
