import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name='parsezeeklogs',
  packages=['parsezeeklogs'],
  version='2.0.0',
  description='A lightweight utility for programmatically reading and manipulating Zeek NSM (Bro NSM) log files and outputting into JSON or CSV format. Also allows easy loading into ELK.',
  author='Dan Gunter',
  author_email='dangunter@gmail.com',
  url='https://github.com/dgunter/parsezeeklogs',
  download_url='https://github.com/dgunter/ParseZeekLogs/archive/2.0.0.tar.gz',
  keywords=['InfoSec', 'Zeek NSM', 'security'],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Security"
  ],
)