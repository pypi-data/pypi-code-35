from setuptools import setup, find_packages

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
  name="python-ucp-cli",
  version='0.1.9',
  install_requires=[
	'Click',
  'requests'
  ],
  entry_points='''
    [console_scripts]
    ucp-cli=ucp_cli:cli
  ''',
  packages=find_packages('./src'),
  py_modules=['ucp_cli', 'commands', 'apis', 'config'],
  classifiers=[
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "License :: OSI Approved :: GNU Affero General Public License v3",
    "Operating System :: OS Independent"
  ],
  long_description=long_description,
  long_description_content_type="text/markdown",
  package_dir={'':'src'},
  url='https://github.com/martencassel/python-ucp-cli',
  author='Mårten Cassel',
  author_email='marten.cassel@conoa.se'
)
