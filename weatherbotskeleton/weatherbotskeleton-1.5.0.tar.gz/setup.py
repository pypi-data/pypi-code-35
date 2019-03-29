"""setup.py for weatherbotskeleton."""
from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, "VERSION"), encoding="utf-8") as f:
    VERSION = f.read().strip()

with open(path.join(HERE, "README.rst")) as f:
    LONG_DESCRIPTION = f.read().strip()

setup(author="Andrew Michaud",
      author_email="bots+weatherbotskeleton@mail.andrewmichaud.com",
      install_requires=[
          "botskeleton>=3.2.4",
          "pycountry>=18.12.8",
          "requests>=2.21.0",
      ],
      python_requires=">=3.6",
      package_data={
          "weatherbotskeleton": ["ZIP_CODES.txt"],
      },
      license="BSD3",
      name="weatherbotskeleton",

      description="Skeleton for weather-based twitterbots",
      long_description=LONG_DESCRIPTION,

      packages=find_packages(),

      url="https://github.com/alixnovosi/weatherbotskeleton",
      version=VERSION)
