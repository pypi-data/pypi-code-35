import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynosql",
    version="0.0.3",
    author="Brian Stajkowski",
    author_email="stajkowski100@gmail.com",
    description="A NOSQL DB Library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stajkowski/pynosql",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
