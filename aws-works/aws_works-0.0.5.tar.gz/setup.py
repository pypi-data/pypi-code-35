import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws_works",
    version="0.0.5",
    author="Guilherme Lana",
    author_email="guih.lana@gmail.com",
    description="A package to access amazon web services in an easy and intuitive way",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guivl/aws_works",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)