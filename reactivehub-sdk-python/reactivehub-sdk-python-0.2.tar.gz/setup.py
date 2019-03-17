from setuptools import setup, setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name='reactivehub-sdk-python',
  version='0.2',
  author='reactivehub.io',
  author_email='luiz.gustavo@reactivehub.io',
  description='reactivehub.io Python SDK',
  long_description='The Reactivehub Python SDK implements the methods needed to publish in the Events API.',
  url='https://github.com/reactivehub-io/reactivehub-sdk-python',
  packages=setuptools.find_packages(),
  license='Apache 2.0',
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
  ],
)