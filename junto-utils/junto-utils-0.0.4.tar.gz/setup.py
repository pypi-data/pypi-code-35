import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="junto-utils",
    version="0.0.4",
    author="Timofey Katalnikov",
    author_email="kattimofey@gmail.com",
    description="Utils for Junto projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/junto-team/JuntoUtils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
