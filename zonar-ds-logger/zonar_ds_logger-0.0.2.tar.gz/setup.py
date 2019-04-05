import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setuptools.setup(
    name="zonar_ds_logger",
    version="0.0.2",
    author="Zonar Systems - Data Services Pod",
    author_email="dspod@zonarsystems.com",
    description="Python logger helper to log in json and redirect flask logs",
    long_description=long_description,
    url="https://github.com/evcallia/zonar_ds_logger.git",
    packages=setuptools.find_packages(where="."),
    install_requires=required_packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
