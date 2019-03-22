# -*- coding: utf-8 -*-

from distutils.core import setup, Extension
from glob import glob
import platform

args = ["-Wno-date-time", "-flto"]

if "64bit" in platform.architecture():
    args.append("-DIS_64BIT")

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
]

with open("Readme.md", "r") as fh:
    long_description = fh.read()

pysfish_module = Extension(
    "pysfish",
    sources=glob("src/*.cpp") + glob("src/syzygy/*.cpp"),
    extra_compile_args=args)

setup(name="pysfish", version="0.0.2",
      description="Seirawan-Stockfish Python wrapper",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Bajusz Tamás",
      author_email="gbtami@gmail.com",
      license="GPL3",
      classifiers=CLASSIFIERS,
      url="https://github.com/gbtami/Seirawan-Stockfish",
      ext_modules=[pysfish_module]
      )
