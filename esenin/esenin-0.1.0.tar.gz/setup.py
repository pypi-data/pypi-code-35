import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="esenin",
    version="0.1.0",
    author="vovapolu",
    author_email="vovapolu@gmail.com",
    description="Python wrapper for esenin.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/esenin-org/esenin-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
)

