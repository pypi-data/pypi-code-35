import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lang2vec",
    version="0.1",
    author="Antonis Anastasopoulos, Patrick Littell, David Mortensen",
    author_email="aanastas@cs.cmu.com",
    description="Returns language vectors",
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
