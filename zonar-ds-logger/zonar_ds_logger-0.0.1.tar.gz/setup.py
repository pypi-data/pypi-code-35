import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zonar_ds_logger",
    version="0.0.1",
    author="Zonar Systems - Data Services Pod",
    author_email="dspod@zonarsystems.com",
    description="Python logger helper to log in json and redirect flask logs",
    long_description=long_description,
    url="https://github.com/evcallia/zonar_ds_logger.git",
    packages=setuptools.find_packages(where="."),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
