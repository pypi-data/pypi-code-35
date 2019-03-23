#!/usr/bin/env python3
import sys

def main():
	if sys.version_info[:2] < (3, 5):
		raise SystemExit("hookcheck requires at least Python 3.5.")
	import setuptools
	setuptools.setup(
		name="hookcheck",
		version="1.0.0",
		description="Method decorators to verify webhooks in Flask.",
		url="https://github.com/chrisgavin/hookcheck/",
		packages=setuptools.find_packages(),
		python_requires=">=3.5",
		classifiers=[
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.5",
			"Programming Language :: Python :: 3.6",
			"Programming Language :: Python :: 3 :: Only",
		],
		install_requires=[
			"flask",
		],
		extras_require={
			"dev": [
				"tox",
				"pytest",
				"pyflakes",
			]
		},
	)

if __name__ == "__main__":
	main()
