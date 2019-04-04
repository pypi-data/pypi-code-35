import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auth1api",
    version="0.0.2",
    author="Brian Li, Mark Lalor, and Yidi Huang",
    author_email="auth1@case.edu",
    description="A library to make requests to your Auth1 instance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)