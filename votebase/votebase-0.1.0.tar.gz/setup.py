#!/usr/bin/env python
from setuptools import setup


setup(
    name='votebase',
    version='0.1.0',
    description='Voting/survey platform',
    long_description=open('README').read(),
    author='Pragmatic Mates',
    author_email='info@pragmaticmates.com',
    maintainer='Pragmatic Mates',
    maintainer_email='info@pragmaticmates.com',
    url='https://bitbucket.org/pragmaticmates/votebase/',
    packages=[
        'votebase',
        'votebase.contrib',
        'votebase.core',
        'votebase.thirdparty'
    ],
    include_package_data=True,
    install_requires=(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Development Status :: 3 - Alpha'
    ],
    license='BSD License',
    keywords="django voting survey",
)
