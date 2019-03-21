import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="distantbytes",
    version="0.0.2",
    author="Thomas Rowntree",
    author_email="thomas.james.rowntree@gmail.com",
    description="Print text to a web terminal viewer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.distantbytes.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
