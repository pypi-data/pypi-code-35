#!/usr/bin/python3 -B
from setuptools import setup, find_packages

setup(name = "webplatform-cli",
   version = "1.0.30",
   description = "CLI used for a webplatform",
   author = "Matthew Owens",
   author_email = "mowens@redhat.com",
   url = "https://github.com/lost-osiris/webplatform-cli",
   packages = find_packages(),
   include_package_data = True,
   install_requires = [
      'docker',
      'pymongo'
   ],
   python_requires='>=3',
   license='MIT',
   scripts = ["webplatform_cli/webplatform-cli"],
   long_description = """TODO""",
   classifiers = [
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
)
