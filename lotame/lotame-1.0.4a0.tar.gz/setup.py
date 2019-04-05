from setuptools import find_packages
from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

setup(name='lotame',
      version='1.0.4a',
      description='Simple python wrapper for LOTAME API',
      install_requires=[
          'httplib2==0.10.3',
          'urllib3>=1.23',
          'requests==2.21.0'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6'
      ],
      keywords=(
          'lotame python wrapper client audience behavior api sdk'),
      url='https://github.com/paulokuong/lotame',
      author='Paulo Kuong',
      author_email='paulo.kuong@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      long_description=long_description)
