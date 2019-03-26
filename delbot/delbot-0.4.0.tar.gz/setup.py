#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import find_packages, setup


def get_version(*file_paths):
    """Retrieves the version from delbot/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version('delbot', '__init__.py')


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.md').read()

try:
    from sphinx.setup_command import BuildDoc
    cmdclass = {
        'docs': BuildDoc
    }
except ImportError:
    cmdclass = {}


setup(
    name='delbot',
    version=version,
    description='A service status blog for SaaS applications',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Mark Steadman',
    author_email='mark@podiant.co',
    url='https://git.steadman.io/podiant/delbot',
    packages=find_packages(
        exclude=['testing']
    ),
    include_package_data=True,
    install_requires=[
        'Click==7.0',
        'Django>=2.1'
    ],
    license='MIT',
    zip_safe=False,
    keywords='delbot',
    cmdclass=cmdclass,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    entry_points={
        'console_scripts': [
            'delbot = delbot.cli:main'
        ]
    }
)
