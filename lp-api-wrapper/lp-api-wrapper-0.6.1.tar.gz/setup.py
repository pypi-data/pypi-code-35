import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="lp-api-wrapper",
    version="0.6.1",
    description="Unofficial LP Data API Wrapper",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/danielkerwin/lp-api-wrapper",
    author="LivePerson",
    author_email="analytics@liveperson.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["lp_api_wrapper"],
    include_package_data=True,
    install_requires=["requests", "pandas", "requests-oauthlib", "peewee"],
)
