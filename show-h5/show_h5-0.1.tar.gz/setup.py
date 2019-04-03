import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="show_h5",
    version="0.1",
    author_email="julia@juliaebert.com",
    description="Command-line interface to preview HDF5 files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jtebert/show_h5",
    packages=setuptools.find_packages(),
    install_requires=[
        'h5py',
        'argparse'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
