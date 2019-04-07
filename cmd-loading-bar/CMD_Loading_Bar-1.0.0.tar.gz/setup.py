from setuptools import setup, find_packages
from os import path


# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='CMD_Loading_Bar',
      version="1.0.0",
      packages=['loading_bar'],
      license='MIT',
      description='A simple yet elegant and feature rich cmd-line (stdout) loading bar.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/JoshWidrick/python-cmd-loading-bar',
      author='Joshua Widrick',
      author_email='jjwidric@buffalo.edu',
)
