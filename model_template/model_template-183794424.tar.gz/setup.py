import os
from setuptools import setup

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

setup(name='model_template',
      version=version,
      description='A abstract Template class for running multiples machine \
                   learning models in the same system.',
      url='https://gitlab.com/bumbleblo/modeltemplate',
      author='Felipe Borges',
      author_email='bumbleblo2013@gmail.com',
      license='MIT',
      packages=['model_template'],
      zip_safe=False)
