import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rndua",
    version="0.0.1",
    author="xdavidwu",
    author_email="xdavidwuph@gmail.com",
    description="A python module that generate random user agent based on rules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xdavidwu/python-rndua",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

