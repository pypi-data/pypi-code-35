from setuptools import setup, find_packages

PACKAGE = "Asi"
NAME = "Asi"
DESCRIPTION = "Ansible Api Warpper"
AUTHOR = "loveshell"
AUTHOR_EMAIL = "idweball@gmail.com"
URL = "https://github.com/idweball/Asi"
VERSION = "1.2.1"

with open("README.md", "r") as f:
	long_description = f.read()

setup(
	name=NAME,
	version=VERSION,
	description=DESCRIPTION,
	long_description=long_description,
	long_description_content_type="text/markdown",
	author=AUTHOR,
	author_email=AUTHOR_EMAIL,
	license="BSD",
	url=URL,
	packages=find_packages(),
	zip_safe=False,
	install_requires=["ansible>=2.7"]
)
