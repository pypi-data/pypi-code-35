from setuptools import setup, find_packages
#from distutils.extension import Extension
from distutils.core import Extension

import os, sys
os.environ['ARCHFLAGS'] = '-Wno-error=unused-command-line-argument-hard-error-in-future'

try:
    from Cython.Distutils import build_ext
except ImportError:
    from distutils.command import build_ext
    use_cython = False
else:
    use_cython = True

cmdclass = {}
ext_modules = []

# make sure Cython code is always freshened up before sdist upload.
from distutils.command.sdist import sdist as _sdist

class sdist(_sdist):
    def run(self):
        # Make sure the compiled Cython files in the distribution are up-to-date
        from Cython.Build import cythonize
        print ("cythonizing...")
        cythonize([])
#'cython/mycythonmodule.pyx'
        _sdist.run(self)
cmdclass['sdist'] = sdist

if use_cython:
    ext_modules += [ Extension('configparsercrypt.memzero', sources=['configparsercrypt/memzero.pyx']), ]
    cmdclass.update({ 'build_ext': build_ext })
    print (cmdclass)
else:
    ext_modules += [ Extension('configparsercrypt.memzero', sources=['configparsercrypt/memzero.c']), ]
try:
    from configparser import ConfigParser, NoSectionError, NoOptionError
except ImportError:
    from configparser import ConfigParser, NoSectionError, NoOptionError

def get_install_requires():
    if sys.version_info >= (3,0):
        install_requires = ['cryptography', 'configparser']
    else:
        install_requires = ['cryptography', 'configparser']
    return install_requires
with open("README.rst", "r") as fh:
    long_description = fh.read()
setup (
    name = "configparsercrypt",
    version = "1.0.2",
    description = "Configuration-oriented encryption toolkit to make secure config files simple",
    url="https://github.com/sonnt85",
    author = "thanhson.rf@gmail.com",
    author_email = "thanhson.rf@gmail.com",
    maintainer = "thanhson.rf@gmail.com",
    maintainer_email = "thanhson.rf@gmail.com",
    cmdclass = cmdclass,
    long_description = long_description,
    long_description_content_type = "text/x-rst",
    ext_modules = ext_modules,
    license = "MIT",
    zip_safe = True,
    packages = find_packages(),
    install_requires = get_install_requires(),
    classifiers = [
         'Programming Language :: Python :: 2',
         'Programming Language :: Python :: 2.7',
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.4',
         'Programming Language :: Python :: 3.5',
         'Programming Language :: Python :: 3.6',
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
    )

