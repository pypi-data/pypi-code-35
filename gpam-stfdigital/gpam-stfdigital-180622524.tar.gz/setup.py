from setuptools import setup
import os

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

setup(name='gpam-stfdigital',
      version=version,
      description='Client for integrate service with STF Digital',
      url='https://supremotribunalfederal.gitlab.io/',
      author='GPAM',
      author_email='gpamunb@gmail.com',
      license='MIT',
      install_requires=[
        'pika',
        'requests',
        'python-consul',
      ],
      packages=[
                'gpamstfdigital',
                ],
      zip_safe=False)
