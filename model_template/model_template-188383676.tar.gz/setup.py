import os
import setuptools

from setuptools import setup

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name='model_template',
      version=version,
      description='A abstract Template class for running multiples machine \
                   learning models in the same system.',
      long_description=long_description,
      long_description_context_type='text/markdown',
      url='https://gitlab.com/bumbleblo/modeltemplate',
      author='Felipe Borges',
      author_email='bumbleblo2013@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      zip_safe=False)
