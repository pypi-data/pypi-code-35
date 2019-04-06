from setuptools import setup, find_packages

with open('README.md', 'r') as f:
	long_description = f.read()

with open('requirements.txt') as f:
	requirements = f.read().splitlines()

setup(
	name='fxapi',
	version='1.1',
	author='Amit Avrahamov',
	author_email='avr.amit02@gmail.com',
	description='FXaPi is a unofficial python module for the site fxp.co.il',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/avramit/FXaPi',
	packages=find_packages(),
	install_requires=requirements
)