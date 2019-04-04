import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deep_data_package",
    version="1.0.0",
    author="Team Deep-Data",
    author_email="seansmith@mines.edu",
    description="Hyperion and AVIRIS: file reader, multiple band indici calculator, and interactive mapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seansmith-mines/Deep-Data/archive/v1.0.0.tar.gz",
    keywords=['deep-data', 'AVIRIS', 'Hyperion', 'spectral'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
