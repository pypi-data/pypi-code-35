import setuptools

name = "scenarios"


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name=name,
    version="0",
    author="QuantumBlack Labs",
    author_email="opensource@quantumblack.com",
    description="scenarios",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.quantumblack.com/",
    license="Apache License 2.0",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
