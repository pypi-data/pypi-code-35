#!/usr/bin/env python3

"""
pyleiades: Python Library for EIA Data Examination & Exhibition

Tools to use with the EIA Monthly Energy Review datasets. This package provides
an API for performing more sophisticated examination and visualization of the
Energy Information Administration (EIA) Monthly Energy Review (MER) datasets.

Data can be accessed directly at the EIA website:
    https://www.eia.gov/totalenergy/data/browser/
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from os import path

package_name = 'pyleiades'
project_dir = path.abspath(path.dirname(__file__))
package_dir = path.join(project_dir, package_name)
# Read the contents of the _version file
with open(path.join(package_dir, '_version')) as version_file:
    version = version_file.read().strip()
# Read the contents of the README file
with open(path.join(project_dir, 'README.md'), encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name=package_name,
    version=version,
    description='An API for examing the EIA Monthly Energy Review datasets.',
    author='Mitch Negus',
    author_email='mitchell.negus.17@gmail.com',
    license='FreeBSD',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mitchnegus/pyleiades',
    packages=['pyleiades', 'pyleiades.utils'],
    scripts=['scripts/update_eia_data.py'],
    include_package_data=True
)
