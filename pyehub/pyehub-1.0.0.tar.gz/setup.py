import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyehub",
    version="1.0.0",
    author_email="revins@uvic.ca",
    description="A program to solve a energy hub model in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/energyincities/python-ehub",
    packages=setuptools.find_packages(),
    install_requires=[
        'pulp',
        'contexttimer',
        'pandas==0.20.1',
        'numpy==1.12.1',
        'PyYAML==3.12',
        'xlrd==1.0.0',
        'jsonschema==2.6.0',
        'pylint',
        'openpyxl',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
