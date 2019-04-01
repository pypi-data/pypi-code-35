import setuptools

with open("README.md", "r") as f:
    long_desc = f.read() 

setuptools.setup(
    name="Selfrope",
    version="1.0.0",
    author="Ryan Broman",
    author_email="ryan@broman.dev",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://broman.dev",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)