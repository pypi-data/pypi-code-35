from distutils.core import setup

from setuptools import find_packages

with open('README.md') as f:
	long_description = f.read()

setup(
	name='gconf',
	version='0.5.5',
	author='Max von Tettenborn',
	author_email='max@vtettenborn.net',
	description='Managing a config globally throughout a Python application',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://gitlab.com/max-tet/gconf',
	license='LICENSE',
	packages=find_packages(),
	install_requires=[
		'pyyaml'
	],
	extras_require={
		'dev': ['pytest']
	},
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Operating System :: OS Independent',
		'Intended Audience :: Developers',
	],
)
