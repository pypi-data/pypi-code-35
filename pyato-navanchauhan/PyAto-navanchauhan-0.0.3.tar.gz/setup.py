import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="PyAto-navanchauhan",
	version="0.0.3",
	author="Navan Chauhan",
	author_email="navanchauhan@gmail.com",
	description="Python Wrapper for Zomato API",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/navanchauhan/PyAto",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
	
