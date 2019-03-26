# from distutils.core import setup
from setuptools import setup

setup(name = "webplatform-cli",
   version = "1.0.3",
   description = "CLI used for a webplatform",
   author = "Matthew Owens",
   author_email = "mowens@redhat.com",
   url = "https://github.com/lost-osiris/webplatform-cli",
   packages = ['lib', 'controller'],
   install_requires = [
      'docker',
      'pymongo'
   ],
   license='MIT',
   scripts = ["controller/webplatform-cli.py"],
   long_description = """TODO""",
   classifiers = [
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
)
