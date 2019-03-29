from glob import glob
import os
from distutils.core import setup, Extension

try:
  from Cython.Distutils import build_ext
except ImportError:
  use_cython = False
else:
  use_cython = True

cmdclass = { }
ext_modules = [ ]

if use_cython:
  ext_modules += [
    Extension(os.path.splitext(f)[0].replace("/", "."), [f])
      for f in glob("vrsubtitlemaker/*/*.pyx")
  ]
  cmdclass.update({ 'build_ext': build_ext })
else:
  ext_modules += [
    Extension(os.path.splitext(f)[0].replace("/", "."), [f])
      for f in glob("vrsubtitlemaker/*/*.c")
  ]


setup(
  name="vrsubtitlemaker",
  version="2.0",
  description="Add subtitle to VR video/images.",
  url="http://github.com/hilcj/vrsubtitlemaker",
  author="hilcj",
  author_email="hilcj0001@gmail.com",
  license="GPL",
  packages=[
    "vrsubtitlemaker",
    "vrsubtitlemaker.create_subtitle_lib",
    "vrsubtitlemaker.add_patterns_lib",
  ],
  install_requires=[
    "numpy",
    "matplotlib",
    "opencv-python",
    "kivy",
    "pillow",
    "pygame",
    "kivy-garden",
  ],
  include_package_data=True,
  scripts=[
    "bin/create_subtitle",
    "bin/add_patterns"
  ],
  zip_safe=False,
  cmdclass=cmdclass,
  ext_modules=ext_modules,
)

os.system("garden install matplotlib --kivy")