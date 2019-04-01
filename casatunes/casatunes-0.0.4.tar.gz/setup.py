import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="casatunes",
    version="0.0.4",
    author="Alexey Ivanov",
    author_email="me@reso.od.ua",
    description="Simple library for CasaTunes REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/resoai/casatunes",
    packages=setuptools.find_packages(),
    install_requires=['validators'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)