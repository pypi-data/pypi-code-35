from setuptools import setup

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
	name='IHpip',
	version='0.1.0',
	packages=['IHpip'],
	url='https://gitlab.com/ire4ever1190/ihpip',
	license='',
	long_description=long_description,
	long_description_content_type="text/markdown",
	author='Jake Leahy',
	author_email='darhyaust@gmail.com',
	description='Small package that makes requirement.txt files better',
	entry_points={
		'console_scripts': [
			'ihpip = IHpip:run'
		]
	},
)
