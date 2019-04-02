#coding=utf8
__doc__ = """uliweb-menu

:copyright: (c) 2016 by Limodou(Limodou AT gmail.com).
:license: BSD, see LICENSE for more details.
"""

import re
import os
import sys

from setuptools import setup
from setuptools.command import build_py as b

def copy_dir(self, package, src, dst):
    self.mkpath(dst)
    for r in os.listdir(src):
        if r in ['.svn', '_svn']:
            continue
        fpath = os.path.join(src, r)
        if os.path.isdir(fpath):
            copy_dir(self, package + '.' + r, fpath, os.path.join(dst, r))
        else:
            ext = os.path.splitext(fpath)[1]
            if ext in ['.pyc', '.pyo', '.bak', '.tmp']:
                continue
            target = os.path.join(dst, r)
            self.copy_file(fpath, target)

def find_dir(self, package, src):
    for r in os.listdir(src):
        if r in ['.svn', '_svn']:
            continue
        fpath = os.path.join(src, r)
        if os.path.isdir(fpath):
            for f in find_dir(self, package + '.' + r, fpath):
                yield f
        else:
            ext = os.path.splitext(fpath)[1]
            if ext in ['.pyc', '.pyo', '.bak', '.tmp']:
                continue
            yield fpath

def build_package_data(self):
    for package in self.packages or ():
        src_dir = self.get_package_dir(package)
        build_dir = os.path.join(*([self.build_lib] + package.split('.')))
        copy_dir(self, package, src_dir, build_dir)
setattr(b.build_py, 'build_package_data', build_package_data)

def get_source_files(self):
    filenames = []
    for package in self.packages or ():
        src_dir = self.get_package_dir(package)
        filenames.extend(list(find_dir(self, package, src_dir)))
    return filenames
setattr(b.build_py, 'get_source_files', get_source_files)

def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname, default=''):
    filename = fpath(fname)
    if os.path.exists(filename):
        return open(fpath(fname)).read()
    else:
        return default


def desc():
    info = read('README.md', __doc__)
    return info + '\n\n' + read('doc/CHANGELOG.md')

file_text = read(fpath('uliweb_menu/__init__.py'))


def grep(attrname):
    pattern = r"{0}\s*=\s*'([^']*)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval

if sys.version_info[0] == 2:
    uliweb_mname = "uliweb"
else:
    uliweb_mname = "uliweb3"

setup(
    name='uliweb-menu',
    version=grep('__version__'),
    url=grep('__url__'),
    license='BSD',
    author=grep('__author__'),
    author_email=grep('__email__'),
    description='uliweb-menu',
    long_description=desc(),
    packages = ['uliweb_menu'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        uliweb_mname, 'uliweb-layout'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)