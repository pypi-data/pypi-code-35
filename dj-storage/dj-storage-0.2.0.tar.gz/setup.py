from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding = 'utf-8') as f:
	long_description = f.read()

setup(
	name = 'dj-storage',
	version = '0.2.0',
	description = 'Nice file storage support for Django',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	url = 'https://gitlab.com/aiakos/dj-storage',
	author = 'Aiakos Contributors',
	author_email = "aiakos@aiakosauth.com",
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Framework :: Django',
		'Framework :: Django :: 2.0',
		'Framework :: Django :: 2.1',
	],
	keywords = 'google storage',
	packages = find_packages(exclude = ['contrib', 'docs', 'tests']),
	zip_safe = True,
	install_requires = ['django>=2.0.0'],
	extras_require = {
		'GCP': ['google-auth'],
	},
)
