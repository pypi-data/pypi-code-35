import os
from setuptools import find_packages, setup


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyTUID',
    version='1.3.4',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Django app for authentication via TUID (CAS)',
    long_description=long_description,
    url='https://github.com/d120/pyTUID',
    author='Fabian Franke',
    author_email='ffranke@d120.de',
    install_requires=[
        'python-cas',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
