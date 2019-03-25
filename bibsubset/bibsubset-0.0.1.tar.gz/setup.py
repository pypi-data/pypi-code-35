# encoding: utf-8
from setuptools import setup, find_packages
pkg = "bibsubset"
ver = '0.0.1'

with open(pkg+'/version.py', 'wt') as h:
    h.write('__version__ = "{}"\n'.format(ver))

setup(
    name             = pkg,
    version          = ver,
    description      = (
        "Extract bibtex subset"),
    long_description = (
        "Have a large bibtex library but you only want to extract the "
        "subsets of entries that are needed for a particular paper "
        "or project? Then this package is for you!"),
    author           = "Eduard Christian Dumitrescu",
    license          = "LGPLv3",
    url              = "https://hydra.ecd.space/eduard/bibsubset/",
    packages         = find_packages(),
    install_requires = [
        'bibtexparser'],
    entry_points     = {
        'console_scripts': ['bibsubset='+pkg+'.bibsubset:main']},
    classifiers      = ["Programming Language :: Python :: 3 :: Only"])

