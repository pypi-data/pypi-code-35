import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tdcc",
    version="0.0.1",
    author="jn8029",
    author_email="warren.y.cheng@gmail.com",
    description="A crawler for structured product information from TDCC (Taiwan).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jn8029/tdcc",
    packages=setuptools.find_packages(),
    install_requires=['bs4', 'requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
