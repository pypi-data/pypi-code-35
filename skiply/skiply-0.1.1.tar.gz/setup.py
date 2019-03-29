from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name='skiply',
	version='0.1.1',
	description='Skiply Library',
	url='https://github.com/skiplyfrance/skiply.git',
	author='Caroline Bouchat',
	author_email='caroline@skiply.fr',
	install_requires=['flask-sqlalchemy'],
	zip_safe=False)