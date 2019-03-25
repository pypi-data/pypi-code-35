from setuptools import setup

setup(
  name='anislbe',
  packages=['anislbe'],
  version='0.1',
  description=("You meant to type ansible. You ended up here. I don't want "
               "anybody being able to use this to hack you. So I made this."),
  author='Joshua "jag" Ginsberg',
  author_email='jag@flowtheory.net',
  url='https://github.com/j00bar/anislbe',
  install_requires=['ansible']
)
