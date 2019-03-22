from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pip-install-test',
      version='0.3',
      description='A minimal stub package to test success of pip install',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/lsst-sqre/sqre-pip_install_test',
      author='Simon Krughoff',
      author_email='krughoff@lsst.org',
      license='MIT',
      packages=['pip_install_test'],
      zip_safe=False)
