from setuptools import setup, find_packages
import os
import sys


here = os.path.dirname(__file__)

version = "0.1.1"
long_description = open(os.path.join(here, "README"), "r").read()


setup(name="pastegevent3",
      version=version,
      description="Run WSGI applications with PasteDeploy and gevent.",
      long_description=long_description,
      classifiers=[
          "Environment :: Plugins",
          "Framework :: Paste",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Topic :: Internet :: WWW/HTTP :: HTTP Servers"
      ],
      keywords="paste wsgi gevent",
      author="Andrey Popp",
      author_email="8mayday@gmail.com",
      url="",
      license="MIT",
      packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
      zip_safe=True,
      install_requires=[
          "gevent",
          "greenlet",
          "PasteDeploy"
      ],
      entry_points="""
      [paste.server_factory]
      gevent = pastegevent.server:server_factory
      gevent_patched = pastegevent.server:server_factory_patched
      """,
      )
