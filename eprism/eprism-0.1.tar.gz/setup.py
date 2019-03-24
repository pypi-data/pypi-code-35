from setuptools import setup

setup(
    name='eprism',           # This is the name of your PyPI-package.
    version='0.1',           # Update the version number for new releases
    scripts=['eprism.py'],   # The name of your scipt, and also the command you'll be using for calling it
    install_requires=[
        'esptool',
        'pyserial'
    ],
)
