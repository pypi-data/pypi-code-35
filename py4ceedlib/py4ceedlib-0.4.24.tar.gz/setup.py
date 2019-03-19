import setuptools
from setuptools import setup

setup(
    name='py4ceedlib',  # This is the name of your PyPI-package.
    version='0.4.24',  # Update the version number for new releases
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.png'],
    },
    packages=setuptools.find_packages()
    #scripts=['py4ceed']  # The name of your scipt, and also the command you'll be using for calling it
)
