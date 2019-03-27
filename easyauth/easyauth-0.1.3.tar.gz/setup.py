#!/usr/bin/env python
# coding=utf-8

# from __future__ import unicode_literals
import sys

from setuptools import setup, find_packages
import easyauth.make_project as make_project

__author__ = __import__('easyauth').__version__


def read_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()


if "sdist" in sys.argv or 'bdist_wheel' in sys.argv or 'bdist_rpm' in sys.argv or 'bdist_wininst' in sys.argv:
    print("preparing project skeleton...")
    make_project.prepare_project_skeleton_for_setup()

setup(
    name='easyauth',
    version=__import__('easyauth').__version__,
    author=__import__('easyauth').__author__,
    author_email='qingfeng0820@sina.com',
    maintainer=__import__('easyauth').__author__,
    maintainer_email='qingfeng0820@sina.com',
    url='https://github.com/qingfeng0820/easyauth',
    license=__import__('easyauth').__license__,
    # packages=find_packages(),
    packages=find_packages(include=['easyauth']),
    include_package_data=False,
    package_data={
        'easyauth': make_project.get_package_data_for_setup('easyauth/static') +
                    make_project.get_package_data_for_setup('easyauth/locale'),
    },
    data_files=make_project.get_data_files_for_setup() + ['requirements.txt', 'test-requirements.txt'],
    description=(
        'A toolkit to set up web application with authentication and authorization functionalities based on Django.'
    ),
    long_description=open('README.rst').read(),
    keywords=['Authentication based on Django', 'Authorization based on Django', 'Python web application Auth'],
    platforms=["all"],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
    ],
    # exclude_package_data={'': ['test', 'note.txt', 'manage.py', 'debug.py', 'db.sqlite3', '.gitignore', '.travis.yml']},
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('test-requirements.txt'),
    entry_points = {
        'console_scripts': [
            'make_project = easyauth.make_project:main',
        ]
    }

)

if "sdist" in sys.argv or 'bdist_wheel' in sys.argv or 'bdist_rpm' in sys.argv or 'bdist_wininst' in sys.argv:
    print("clean prepared project skeleton")
    make_project.clean_prepared_project_skeleton_after_setup()
