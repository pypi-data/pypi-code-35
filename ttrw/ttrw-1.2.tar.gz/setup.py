import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ttrw",
    version="1.2",
    author="Tomasz Taraś",
    author_email="tomasztaras@outlook.com",
    description="Simple python package that generates strings with randomly selected words.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ttomasz/ttrw",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True
)
