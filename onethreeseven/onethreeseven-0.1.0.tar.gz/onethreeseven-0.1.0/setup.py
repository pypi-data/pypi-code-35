import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="onethreeseven",
    version="0.1.0",
    author="Piotr Oleskiewicz",
    author_email="piotr@oleskiewi.cz",
    description="package for 137 cloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oleskiewicz/onethreeseven-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
