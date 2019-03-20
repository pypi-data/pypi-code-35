import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyUSDforex",
    version="0.1.0",
    author="Lawrence Stewart",
    author_email="lawrence@lawrencestewart.ca",
    description="Converts foreign fiat currencies to USD by getting and caching hourly exchanges rates from openexchangerates.org",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/getorca/pyUSDforex",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)