#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from setuptools import setup
from setuptools import Extension

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

is_64bits = sys.maxsize > 2**32

sptop = '../..'
ccopts = []
# ccdefs = [('SWIGRUNTIME_DEBUG', 1)]
ccdefs = []
ldopts = []
libpath = sptop + '/lib'
ext_include_dirs = [sptop + '/spAudio', sptop + '/spBase', sptop + '/include']

if not os.path.isfile('_spaudio/spaudio_c_wrap.c') \
   or not os.path.isfile('_spaudio/spaudio_c.py'):
    ext_sources = ['_spaudio/spaudio_c.i', '_spaudio/spaudio_c.c']
else:
    ext_sources = ['_spaudio/spaudio_c_wrap.c', '_spaudio/spaudio_c.c']

if sys.platform == 'win32':
    # ldopts = ['/DEBUG', '/OPT:REF', '/OPT:ICF']
    # ccopts = ['/Zi']
    ext_libraries = ['spAudio', 'spBase', 'winmm',
                     'shell32', 'User32', 'Kernel32']
    if is_64bits:
        libpath = sptop + '/lib/x64/v141'
    else:
        libpath = sptop + '/lib/v141'
        #libpath = sptop + '/lib/v120_xp'
elif sys.platform == 'darwin':
    import subprocess
    sdktop = subprocess.getoutput('xcrun --sdk macosx --show-sdk-path')
    ldopts = ['--sysroot=' + sdktop, '-Wl,-framework,AudioToolbox',
              '-Wl,-framework,AudioUnit', '-Wl,-framework,CoreAudio']
    if is_64bits:
        ext_libraries = ['spa.mac64', 'spb.mac64']
    else:
        ext_libraries = ['spa.mac-ub', 'spb.mac-ub']
else:
    if is_64bits:
        ext_libraries = ['spa.linux64', 'spb.linux64']
    else:
        ext_libraries = ['spa.linux-glibc', 'spb.linux-glibc']

ext_spaudio = Extension(
    '_spaudio._spaudio_c',
    ext_sources,
    swig_opts=['-threads', '-modern', '-I' + sptop + '/spAudio',
               '-I' + sptop + '/spBase', '-I' + sptop + '/include'],
    include_dirs=ext_include_dirs,
    define_macros=ccdefs,
    extra_compile_args=ccopts,
    extra_link_args=ldopts,
    libraries=ext_libraries,
    library_dirs=[libpath]
)

setup(
    name='spaudio',
    version='0.7.13-3',
    description='spAudio audio I/O library',
    long_description=readme,
    long_description_content_type='text/x-rst',
    url='http://www-ie.meijo-u.ac.jp/labs/rj001/spLibs/python/spAudio/en/index.html',
    keywords=['audio', 'sound', 'play', 'record', 'I/O'],
    ext_modules=[ext_spaudio],
    py_modules=['spaudio'],
    packages=['_spaudio'],
    install_requires=[''],
    extras_require={'numpy': ['numpy']},
    author='Hideki Banno',
    author_email='banno@meijo-u.ac.jp',
    license='MIT',
    platforms=['posix', 'nt'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Sound/Audio',
    ],
)
