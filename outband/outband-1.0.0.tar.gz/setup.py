#!/usr/bin/env python3
import sys

def main():
	if sys.version_info[:2] < (3, 5):
		raise SystemExit("outband requires at least Python 3.5.")
	import setuptools
	setuptools.setup(
		name="outband",
		version="1.0.0",
		description="Connect to an out-of-band management KVM console from the command line.",
		url="https://github.com/chrisgavin/outband/",
		packages=setuptools.find_packages(),
		python_requires=">=3.5",
		classifiers=[
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.5",
			"Programming Language :: Python :: 3.6",
			"Programming Language :: Python :: 3 :: Only",
		],
		install_requires=[
			"lxml",
			"requests",
		],
		extras_require={
			"dev": [
				"tox",
				"mypy",
				"pyflakes",
			]
		},
		entry_points={
			"console_scripts":[
				"outband = outband.__main__:main",
			],
		},
	)

if __name__ == "__main__":
	main()
