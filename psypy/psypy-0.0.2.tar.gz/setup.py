import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="psypy",
    version="0.0.2",
    author="Will Long",
    author_email="long@latech.edu",
    description="Python library for calculating psychrometric states of moist air.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/longapalooza/psypy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)