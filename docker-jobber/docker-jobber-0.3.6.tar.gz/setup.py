# To install for "editing":
#   pip install -e .
# Regular install:
#   pip install --user .	# Just for user
#		or
#	pip install .			# For everyone

from setuptools import find_packages, setup

with open('DESCRIPTION.md', 'r') as inf:
	DESCRIPTION = inf.read()

setup(
	name = 'docker-jobber',
	version='0.3.6',		# NOTE Keep synced with __version__ in jobber/__init__.py
	author="Eric Parker",
	author_email="eric.parker@mentice.com",
	description="A command line interface (CLI) application for managing machine learning workflows using Docker",
	long_description=DESCRIPTION,
	long_description_content_type='text/markdown',
	url="https://github.com/mentice/docker-jobber",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: BSD License",
		"Operating System :: OS Independent",
		"Topic :: Scientific/Engineering :: Artificial Intelligence"
	],
	packages=find_packages('src'),
	package_dir={'':'src'},
	include_package_data=True,
	install_requires=['PyYAML', 'async-timeout', 'jsonmerge', 'click', 'docker'],
	entry_points = {
		'console_scripts': [
			'jobber=cli.cli:cli',
		],
	},
)