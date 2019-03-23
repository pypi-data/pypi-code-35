import setuptools

long_description=""
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="argparse-graph",
    version="0.1.1",
    author="Quentin Le Baron",
    author_email="quentin.le-baron@epitech.eu",
    license="Apache 2.0",
    description="yaml file to add logique with argparse object.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["yamllint"],
    url="https://github.com/kuty22/argparse_graph",
    tests_require=["pytest"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
