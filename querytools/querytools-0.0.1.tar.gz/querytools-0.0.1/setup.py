import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="querytools",
    version="0.0.1",
    author="Jake Thomas",
    author_email="jake@bostata.com",
    description="Tools for querying data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bostata.com/",
    packages=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
