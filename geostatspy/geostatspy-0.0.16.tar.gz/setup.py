import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geostatspy",
    version="0.0.16",
    author="Michael Pyrcz",
    author_email="mpyrcz@austin.utexas.edu",
    description="Geostatistical methods for spatial modeling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GeostatsGuy/GeostatsPy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)