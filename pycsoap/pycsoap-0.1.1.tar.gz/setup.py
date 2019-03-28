from setuptools import find_packages, Extension

#!/usr/bin/env python
try:
    from setuptools import setup
    args = {}
except ImportError:
    from distutils.core import setup
    print("""\
*** WARNING: setuptools is not found.  Using distutils...
""")
 
from setuptools import setup
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

ext_list = []
for extname, soname in zip(
    [
        "src/soapAnalFullPySigma.c",
        "src/soapGTO.c",
        "src/soapGeneral.c",
    ],
    [
        "src.libsoapPySig",
        "src.libsoapGTO",
        "src.libsoapGeneral",
    ]):
    ext_list.append(Extension(soname,
        [extname],
        include_dirs=["src"],
        extra_compile_args=["-O3", "-std=c99"]
    ))


extensions = ext_list




from os import path
setup(name='pycsoap',
      version='0.1.1',
      description='Generation of SOAP descriptors.',
      long_description= "" if not path.isfile("README.md") else read_md('README.md'),
      author='Andrew H Nguyen',
      author_email='andrewhuynguyen10@gmail.com',
      url='https://gitlab.com/andrewhuynguyen/pycsoap',
      license='BSD 3-clause New or Revised License',
      setup_requires=[],
      tests_require=['pytest'],
      install_requires=[
          "pyparsing",
          "argparse",
          "termcolor",
          "six",
          "numpy",
          "scipy",
          "future",
          "ase"
      ],
      packages=['pycsoap'],
      scripts=[],
      #package_data={'src': []},
      #include_package_data=True,
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: BSD License',
          'Operating System :: MacOS',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: C',
          'Topic :: Scientific/Engineering',
      ],
      ext_modules=extensions,

	zip_safe=False
     )
