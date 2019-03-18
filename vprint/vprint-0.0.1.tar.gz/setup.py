import os
from setuptools import find_packages, setup
from distutils.util import convert_path


def get_version(pkg_name):
    ver_path = convert_path('{}/version.py'.format(pkg_name))
    with open(ver_path) as ver_file:
        text = ver_file.read()
    try:
        ver = text.split('version = ')[1]
    except IndexError:
        raise RuntimeError('Could not parse version string: {}'.format(text))
    ver = ver.replace('\n', '').strip().strip('"').strip("'")
    return ver

# The directory containing this file
HERE = os.path.dirname(__file__)
with open(os.path.join(HERE, 'README.md')) as fp:
    README = fp.read()


classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
]

pkg_name = 'vprint'
setup(
    name='vprint',
    version=get_version('vprint'),
    description='Verbose Printing Utility',
    author='Michael McDermott',
    license='MIT',
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url='https://github.com/xkortex/vprint'

)
