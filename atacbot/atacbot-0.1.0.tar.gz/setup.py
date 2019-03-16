#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ["pyTelegramBotAPI"]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Flavio Elawi",
    author_email='flavio.elawi@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A telegram bot to query muovi.roma.it",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='atacbot',
    name='atacbot',
    packages=find_packages(include=['atacbot']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/flavioelawi/Telegram-atacbot',
    version='0.1.0',
    zip_safe=False,
    entry_points = {
        'console_scripts': ['atacbot_run=atacbot.atacbot:start'],
    }
)
