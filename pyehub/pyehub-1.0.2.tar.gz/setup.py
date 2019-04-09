import setuptools

with open("python-ehub/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyehub",
    version="1.0.2",
    author_email="revins@uvic.ca",
    description="A library used to solve an energy hub model in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/energyincities/python-ehub",
    packages=setuptools.find_packages(),
    install_requires=[
        'pulp',
        'contexttimer',
        'pandas',
        'numpy',
        'PyYAML',
        'xlrd',
        'jsonschema',
        'pylint',
        'openpyxl',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
