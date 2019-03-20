"""Setup script for cryptofinance"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="cryptofinance",
    version="0.0.1",
    description="One API connecting you to cryptocurrency exchanges, indices, on-chain and social data.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cryptofinance-ai/cryptofinance-api",
    author="CRYPTOFINANCE",
    author_email="support@cryptofinance.ai",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Office/Business :: Financial",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries"
    ],
    packages=["cryptofinance"],
    include_package_data=True,
    install_requires=[
        "requests", "ujson"
    ]
)
