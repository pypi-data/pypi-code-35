from setuptools import setup
from setuptools import find_packages
from os import path

name = 'eloqua-formhandler'
version = '0.9'
release = '0.9a0'

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name=name,
    version=release,
    description='Validate and send Oracle Eloqua Forms.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://gitlab.com/intheflow/python-eloqua-formhandler',
    author='Florian Schweikert',
    author_email='florian.schweikert@zumtobelgroup.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=['tests']),
    install_requires=['requests', 'structlog', 'attrs'],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'docs/source'),
            'build_dir': ('setup.py', 'docs/build')}}
)
