# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='bert-deid',
      version='0.1.2',
      description='Find personal identifiers in text with BERT',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/MIT-LCP/pydeid',
      keywords='deid pydeid deidentification de-identification EHR',
      license='MIT',
      packages=find_packages(),
      install_requires=[]
    )