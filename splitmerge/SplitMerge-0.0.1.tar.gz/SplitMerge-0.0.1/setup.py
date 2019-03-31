import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SplitMerge",
    version="0.0.1",
    author="Satyaki De",
    author_email="satyaki.de@gmail.com",
    description="Split & Merge utilities for large csv files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/SplitMerge",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)