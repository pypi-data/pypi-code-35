import os
import sys

from setuptools import setup, find_packages

PROJECT_NAME = 'PopulateData'
MODULE_NAME = 'populatedata'

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

setup(
    name='PopulateData',
    version='1.0.0',

    author='JuneSunshine',
    author_email='ljygeek@gmail.com',

    description='Populate / generate data based on certain conditions',
    long_description='Populate / generate data based on certain conditions',
    keywords='populatedata python3 package',

    url='https://github.com/JuneSunshine/Magic_Square',
    license="MIT Licence",

    platforms='all',

    packages=find_packages(),
    include_package_data=True,

)