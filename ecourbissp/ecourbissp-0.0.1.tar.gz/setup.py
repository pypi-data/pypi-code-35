import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ecourbissp",
    version="0.0.1",
    author="Julio Manuel Blanco Perez",
    author_email="jblancoperez@gmail.com",
    description="Get São Paulo Eco urbis schedules from Official Site",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jblancoperez/ecourbissp",
    install_requires = ['requests==2.21.0'],
    packages=['ecourbissp'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

