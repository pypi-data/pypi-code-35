"""
установка пакета pyeco, в папке с setup.py ->
pip3 install --upgrade .
"""

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pyeco',
      version='0.5',
      description='useful python things',
      long_description=long_description, 
      long_description_content_type='text/markdown',   
      author='Nikita Kuzin',
      author_email='getsense@yandex.ru',
      packages=['pyeco'],
      zip_safe=False)
