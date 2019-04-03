from setuptools import setup

__version__ = 1.3
__author__ = 'R. THOMAS'
__licence__ = 'GPLv3'
__credits__ = "Romain Thomas"
__maintainer__ = "Romain Thomas"
__website__ = 'https://github.com/astrom-tom/catmatch'
__email__ = "the.spartan.proj@gmail.com"
__status__ = "released"
__year__ = '2019'

setup(
   name = 'catmatch',
   version = __version__,
   author = __credits__,
   packages = ['catmatch'],
   entry_points = {'gui_scripts': ['catmatch = catmatch.__main__:main',],},
   description = 'A simple catalog matching script',
   python_requires = '>=3.6',
   install_requires = [
       "numpy >= 1.16",
       "catscii>= 1.1",
   ],
   include_package_data=True,
)
