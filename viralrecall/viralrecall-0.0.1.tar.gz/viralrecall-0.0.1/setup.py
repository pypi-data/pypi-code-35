import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="viralrecall",
    version="0.0.1",
    author="Frank Aylward",
    author_email="faylward@vt.edu",
    description="Tool for predicting prophage and other virus-like regions in genomic data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/faylward/viralrecall",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: Unix",
    ],
)