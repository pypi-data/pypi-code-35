import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iotnode",
    version="0.0.4",
    author="Ben Hussey",
    author_email="ben@blip2.net",
    description="Framework for running embedded code with multiple modular sources of data input/output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blip2/iotnode",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
